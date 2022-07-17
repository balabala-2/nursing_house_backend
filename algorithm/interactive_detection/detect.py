import cv2
import dlib
import numpy as np
from fastapi.responses import StreamingResponse

from algorithm.deepface.commons import functions
from algorithm.deepface.detectors import FaceDetector
from algorithm.interactive_detection.audio import Audio_detection
from algorithm.utils.global_variable import *
from dao.scene_operation import add_interactive
from dao.user_head_img_operation import get_head_feature
from schemas.other import Interactive_info

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
from algorithm.deepface import DeepFace


# Author:   coneypo
# Blog:     http://www.cnblogs.com/AdaminXie
# GitHub:   https://github.com/coneypo/Dlib_face_recognition_from_camera
# Mail:     coneypo@foxmail.com

class Interactive_detection:
    """陌生人识别
    """

    def __init__(self) -> None:
        stream = cv2.VideoCapture(interactive_detection_url)
        stream.set(3, video_width)
        stream.set(4, video_height)
        self.stream = stream
        # 用来存放所有录入人脸特征的数组
        self.face_features_known_list = []
        # 存储录入人脸名字
        self.face_name_known_list = []
        # 存储人的id
        self.face_id_known_list = []

        # 用来存储上一帧和当前帧 ROI 的质心坐标 / List to save centroid positions of ROI in frame N-1 and N
        self.last_frame_face_centroid_list = []
        self.current_frame_face_centroid_list = []

        # 用来存储上一帧和当前帧检测出目标的名字 / List to save names of objects in frame N-1 and N
        self.last_frame_face_name_list = []
        self.current_frame_face_name_list = []

        # 上一帧和当前帧中人脸数的计数器 
        self.last_frame_face_cnt = 0
        self.current_frame_face_cnt = 0

        # 用来存放进行识别时候对比的欧氏距离 
        self.current_frame_face_X_e_distance_list = []

        # 存储当前摄像头中捕获到的所有人脸的坐标名字
        self.current_frame_face_position_list = []
        # 存储当前摄像头中捕获到的人脸特征 / Save the features of people in current frame
        self.current_frame_face_feature_list = []

        # e distance between centroid of ROI in last and current frame
        self.last_current_frame_centroid_e_distance = 0

        # 控制再识别的后续帧数
        # 如果识别出 "unknown" 的脸, 将在 reclassify_interval_cnt 计数到 reclassify_interval 后, 对于人脸进行重新识别
        self.reclassify_interval_cnt = 0
        self.reclassify_interval = 10

        self.happy_frame = None
        self.happy_value = 0

        self.volunteer_id = -1
        self.elderly_id = -1
        Audio_detection.init()

    # 从 数据库 读取录入人脸特征
    def get_face_feature(self):
        _, _, results = get_head_feature()
        self.face_name_known_list = ['_'.join([str(i) for i in item]) for item in
                                     zip(results['user_types'], results['user_ids'])]
        self.face_features_known_list = results['user_features']

    @staticmethod
    # 计算两个128D向量间的欧式距离
    def return_euclidean_distance(feature_1, feature_2):
        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
        return dist

        # 使用质心追踪来识别人脸

    def centroid_tracker(self):
        for i in range(len(self.current_frame_face_centroid_list)):
            e_distance_current_frame_person_x_list = []
            # 对于当前帧中的人脸1, 和上一帧中的 人脸1/2/3/4/.. 进行欧氏距离计算
            for j in range(len(self.last_frame_face_centroid_list)):
                self.last_current_frame_centroid_e_distance = self.return_euclidean_distance(
                    np.array(self.current_frame_face_centroid_list[i]), np.array(self.last_frame_face_centroid_list[j]))

                e_distance_current_frame_person_x_list.append(
                    self.last_current_frame_centroid_e_distance)

            last_frame_num = e_distance_current_frame_person_x_list.index(
                min(e_distance_current_frame_person_x_list))
            self.current_frame_face_name_list[i] = self.last_frame_face_name_list[last_frame_num]

    def run_video(self):
        # 1. 读取人脸特征
        self.get_face_feature()
        cnt = 0
        pre_emotion_predictions = None
        while True:
            ret, img = self.stream.read()
            if not ret:
                break
            img = cv2.resize(img, (640, 480))
            if cnt == 0:
                cnt = 3
                # 2. 检测人脸
                faces = FaceDetector.detect_faces(face_detector, detector_backend, img, align=False)

                # 3. 更新人脸计数器
                self.last_frame_face_cnt = self.current_frame_face_cnt
                self.current_frame_face_cnt = len(faces)

                # 4. 更新上一帧中的人脸列表
                self.last_frame_face_name_list = self.current_frame_face_name_list[:]

                # 5. 更新上一帧和当前帧的质心列表
                self.last_frame_face_centroid_list = self.current_frame_face_centroid_list
                self.current_frame_face_centroid_list = []

                # 6.1 如果当前帧和上一帧人脸数没有变化
                if (self.current_frame_face_cnt == self.last_frame_face_cnt) and (
                        self.reclassify_interval_cnt != self.reclassify_interval):

                    self.current_frame_face_position_list = []

                    if "unknown" in self.current_frame_face_name_list:
                        self.reclassify_interval_cnt += 1

                    if self.current_frame_face_cnt != 0:
                        for _, (x, y, w, h) in faces:
                            left, right, top, bottom = x, x + w, y, y + h
                            self.current_frame_face_position_list.append(tuple(
                                [left, int(bottom + h / 4)]))
                            self.current_frame_face_centroid_list.append(
                                [int(left + right) / 2, int(top + bottom) / 2])

                    # 如果当前帧中有多个人脸, 使用质心追踪
                    if self.current_frame_face_cnt != 1:
                        self.centroid_tracker()

                    happy_value = 0
                    for i, (_, (x, y, w, h)) in enumerate(faces):
                        cv2.rectangle(img, (x, y), (x + w, y + h), (67, 67, 67), 1)
                        # facial attribute analysis
                        cur_face_name = self.current_frame_face_name_list[i]
                        cv2.putText(img, cur_face_name, (x + 10, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                        if 'volunteer' in cur_face_name:
                            self.volunteer_id = int(cur_face_name.split('_')[1])
                        elif 'elderly' in cur_face_name:
                            self.elderly_id = int(cur_face_name.split('_')[1])

                        gray_img = functions.preprocess_face(img =img[y:y + h, x:x + w], target_size = (48, 48), grayscale = True, enforce_detection = False, detector_backend=detector_backend)
                        emotion_predictions = emotion_model.predict(gray_img, verbose=0)[0, :]
                        happy_value += emotion_predictions[3]
                        pre_emotion_predictions = emotion_predictions

                    if happy_value > self.happy_value:
                        self.happy_frame = img
                        self.happy_value = happy_value

                # 6.2 如果当前帧和上一帧人脸数发生变化
                else:
                    self.current_frame_face_position_list = []
                    self.current_frame_face_X_e_distance_list = []
                    self.current_frame_face_feature_list = []
                    self.reclassify_interval_cnt = 0

                    # 6.2.1 人脸数减少
                    if self.current_frame_face_cnt == 0:
                        self.current_frame_face_name_list = []
                    # 6.2.2 人脸数增加
                    else:
                        self.current_frame_face_name_list = []
                        for _, (x, y, w, h) in faces:
                            shape = face_landmarks_extractor(img, dlib.rectangle(x, y, x + w, y + h))
                            self.current_frame_face_feature_list.append(
                                np.array(face_feature_extractor.compute_face_descriptor(img, shape)))
                            self.current_frame_face_name_list.append("unknown")

                        # 6.2.2.1 遍历捕获到的图像中所有的人脸
                        for k, (_, (x, y, w, h)) in enumerate(faces):
                            left, right, top, bottom = x, x + w, y, y + h
                            self.current_frame_face_centroid_list.append(
                                [int(left + right) / 2, int(top + bottom) / 2])
                            self.current_frame_face_X_e_distance_list = []
                            # 6.2.2.2 每个捕获人脸的名字坐标
                            self.current_frame_face_position_list.append(tuple(
                                [left, int(bottom + (h) / 4)]))

                            # 6.2.2.3 对于某张人脸, 遍历所有存储的人脸特征
                            for i in range(len(self.face_features_known_list)):
                                e_distance_tmp = self.return_euclidean_distance(
                                    self.current_frame_face_feature_list[k],
                                    self.face_features_known_list[i])
                                self.current_frame_face_X_e_distance_list.append(e_distance_tmp)

                            # 6.2.2.4 寻找出最小的欧式距离匹配
                            if len(self.current_frame_face_X_e_distance_list) > 0:
                                similar_person_num = self.current_frame_face_X_e_distance_list.index(
                                    min(self.current_frame_face_X_e_distance_list))

                                if min(self.current_frame_face_X_e_distance_list) < 0.4:
                                    self.current_frame_face_name_list[k] = self.face_name_known_list[similar_person_num]

                # cv2.imshow('img', img)
                yield cv2.imencode('.jpg', img)[1].tobytes()
            else:
                happy_value = 0
                for i, (_, (x, y, w, h)) in enumerate(faces):
                    cv2.rectangle(img, (x, y), (x + w, y + h), (67, 67, 67), 1)
                    # facial attribute analysis
                    cur_face_name = self.current_frame_face_name_list[i]
                    cv2.putText(img, cur_face_name, (x + 10, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    if 'volunteer' in cur_face_name:
                        self.volunteer_id = int(cur_face_name.split('_')[1])
                    elif 'elderly' in cur_face_name:
                        self.elderly_id = int(cur_face_name.split('_')[1])
                    emotion_predictions = pre_emotion_predictions
                    if emotion_predictions is not None:
                        happy_value += emotion_predictions[3]

                if happy_value > self.happy_value:
                    self.happy_frame = img
                    self.happy_value = happy_value
            cnt -= 1
        yield None

    def close_stream(self):
        self.stream.release()

    def generate_frame(self):
        """Video streaming generator function."""
        frames = self.run_video()
        while True:
            frame = frames.__next__()
            if frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                if self.happy_frame is not None:
                    add_interactive(Interactive_info(volunteer_id=self.volunteer_id, elderly_id=self.elderly_id,
                                                     img=cv2.imencode('.jpg', self.happy_frame)[1].tobytes(),
                                                     text=Audio_detection.text))
                break

    def video_generate(self):
        if self.stream.isOpened():
            return StreamingResponse(self.generate_frame(),
                                     media_type='multipart/x-mixed-replace; boundary=frame')
        else:
            def file():
                with open('resources/video_not_open.jpg', mode='rb') as f:
                    yield from f

            return StreamingResponse(file(), media_type='image/jpg')
