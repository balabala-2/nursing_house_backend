from threading import Thread

import cv2
import mediapipe as mp
import numpy as np
import torch
from fastapi.responses import StreamingResponse
from torchvision import transforms

from algorithm.deepface.detectors import FaceDetector
from algorithm.face_detection.pfld.dectect import point_line, point_point, get_num, tran, mouth_aspect_ratio
from algorithm.face_detection.pfld.face_feature import Face_feature
from algorithm.face_detection.pfld.pfld import PFLDInference
from algorithm.utils.audioplayer import play_audio
from algorithm.utils.global_variable import device, video_width, video_height, facepose_weights
from dao.user_head_img_operation import add_user_head_img, add_user_head_feature
from schemas.other import User_head_feature_info, User_head_image_info


class Face_pose():
    """_summary_
    检测人的脸部动作，比如抬头低头等，然后进行图片的采集，特征的提取，数据库的存储
    Returns:
        _type_: _description_
    """
    eyeList = [22, 23, 24, 26, 110, 130, 157, 158, 159, 160, 161, 243]  # 左眼
    mouthList = [78, 81, 13, 311, 308, 402, 14, 178]  # 嘴
    checkpoint = torch.load(facepose_weights['model'], map_location=device)
    plfd_backbone = PFLDInference().to(device)
    plfd_backbone.load_state_dict(checkpoint['plfd_backbone'])
    plfd_backbone.eval()
    plfd_backbone = plfd_backbone.to(device)
    transform = transforms.Compose([transforms.ToTensor()])

    face_mesh = mp.solutions.face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    face_feasture = Face_feature()

    detector_backend = 'ssd'
    # 人脸识别模型
    face_detector = FaceDetector.build_model(detector_backend)

    # 动作列表
    action = ['start_image_capturing', 'look_left', 'look_right', 'bow_head', 'rise_head', 'blink', 'open_mouth',
              'end_capturing']

    def __init__(self, face_video_info) -> None:
        """人物脸部动作识别，比如眨眼，张嘴等

        Args:
            user_type (_type_): 用户类型，elderly，staff等
            user_id (_type_): 用户id
        """

        self.ratioList = []  # 存放实时的人眼开合百分比
        self.blinkCounter = 0  # 眨眼计数器默认=0
        self.blinkCounter1 = 0  # 眨眼计数器默认=0
        self.counter = 0  # 代表当前帧没计算过眨眼次数
        self.counter1 = 0  # 代表当前帧没计算过眨眼次数

        # 记录当前进行到第几个action
        self.action_idx = 0

        self.stream = cv2.VideoCapture(0)
        self.stream.set(3, video_width)
        self.stream.set(4, video_height)

        self.frames = []
        self.face_video_info = face_video_info

    def cal_yaw_pitch(self, frame):
        height, width = frame.shape[:2]

        faces = FaceDetector.detect_faces(Face_pose.face_detector, Face_pose.detector_backend, frame, align=False)
        if len(faces) == 1:
            x1, y1, w, h = faces[0][1]
            x2, y2 = x1 + w, y1 + h

            size = int(max([w, h]))
            cx, cy = x1 + w / 2, y1 + h / 2
            x1 = cx - size / 2
            x2 = x1 + size
            y1 = cy - size / 2
            y2 = y1 + size

            dx = max(0, -x1)
            dy = max(0, -y1)
            x1 = max(0, x1)
            y1 = max(0, y1)

            edx = max(0, x2 - width)
            edy = max(0, y2 - height)
            x2 = min(width, x2)
            y2 = min(height, y2)

            cropped = frame[int(y1):int(y2), int(x1):int(x2)]
            if (dx > 0 or dy > 0 or edx > 0 or edy > 0):
                cropped = cv2.copyMakeBorder(cropped, int(dy), int(edy), int(dx), int(edx), cv2.BORDER_CONSTANT, 0)

            cropped = cv2.resize(cropped, (112, 112))

            input = cv2.resize(cropped, (112, 112))
            input = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
            input = self.transform(input).unsqueeze(0).to(device)
            _, landmarks = self.plfd_backbone(input)
            pre_landmark = landmarks[0]
            pre_landmark = pre_landmark.cpu().detach().numpy().reshape(-1, 2) * [112, 112]
            point_dict = {}
            i = 0
            for (x, y) in pre_landmark.astype(np.float32):
                point_dict[f'{i}'] = [x, y]
                i += 1

            # yaw
            point1 = [get_num(point_dict, 1, 0), get_num(point_dict, 1, 1)]
            point31 = [get_num(point_dict, 31, 0), get_num(point_dict, 31, 1)]
            point51 = [get_num(point_dict, 51, 0), get_num(point_dict, 51, 1)]
            crossover51 = point_line(point51, [point1[0], point1[1], point31[0], point31[1]])
            yaw_mean = point_point(point1, point31) / 2
            yaw_right = point_point(point1, crossover51)
            yaw = (yaw_mean - yaw_right) / yaw_mean
            yaw = int(yaw * 71.58 + 0.7037)

            # pitch
            pitch_dis = point_point(point51, crossover51)
            if point51[1] < crossover51[1]:
                pitch_dis = -pitch_dis
            pitch = int(1.497 * pitch_dis + 18.97)

            return yaw, pitch
        return 0, 0

    def blink_or_mouth(self, multi_face_landmarks):
        for face_landmarks in multi_face_landmarks:
            leftUpx, leftUpy = tran(face_landmarks.landmark[159])
            leftDownx, leftDowny = tran(face_landmarks.landmark[23])
            leftLeftx, leftLefty = tran(face_landmarks.landmark[130])
            leftRightx, leftRighty = tran(face_landmarks.landmark[243])

            r1 = pow(pow(leftUpx - leftDownx, 2) + pow(leftUpy - leftDowny, 2), 0.5)
            r2 = pow(pow(leftLeftx - leftRightx, 2) + pow(leftLefty - leftRighty, 2), 0.5)

            # 计算竖直距离与水平距离的比值
            ratio = 100 * r1 / r2
            self.ratioList.append(ratio)

            # （5）平滑实时变化曲线
            if len(self.ratioList) > 10:
                self.ratioList.pop(0)
            ratioAvg = sum(self.ratioList) / len(self.ratioList)

            # 张嘴
            if mouth_aspect_ratio(face_landmarks.landmark, Face_pose.mouthList) > 0.7:
                return 0, 1
            # 眨眼
            if ratioAvg < 30:
                return 1, 0

        return 0, 0

    def run(self):
        frames = []  # 左边，右边，低头，抬头, 眨眼，张嘴

        ret, frame = self.stream.read()

        # 音频线程
        audio_thread = Thread(target=play_audio, args=(f'resources/audios/{Face_pose.action[self.action_idx]}.mp3',))
        audio_thread.start()

        next_video = False

        while ret:
            frame = cv2.flip(frame, 1)

            cv2.putText(frame, Face_pose.action[self.action_idx], (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                        (0, 255, 0), 2)

            if self.action_idx <= 4:
                yaw, pitch = self.cal_yaw_pitch(frame)
            else:
                results = Face_pose.face_mesh.process(frame)
                if results.multi_face_landmarks:
                    eye_blink, mouth_open = self.blink_or_mouth(results.multi_face_landmarks)

            if not audio_thread.is_alive():
                if self.action_idx == 0:
                    self.action_idx += 1
                    next_video = True
                elif (self.action_idx == 1 and yaw > 20) or \
                        (self.action_idx == 2 and yaw < -20) or \
                        (self.action_idx == 3 and pitch > 30) or \
                        (self.action_idx == 4 and pitch < -10) or \
                        (self.action_idx == 5 and eye_blink == 1) or \
                        (self.action_idx == 6 and mouth_open == 1) or \
                        (self.action_idx == 7) and not next_video:
                    frames.append(frame)
                    next_video = True
                    self.action_idx += 1

                if next_video:
                    next_video = False
                    if self.action_idx >= len(Face_pose.action):
                        break
                    audio_thread = Thread(target=play_audio,
                                          args=(f'resources/audios/{Face_pose.action[self.action_idx]}.mp3',))
                    audio_thread.start()

            yield cv2.imencode('.jpg', frame)[1].tobytes()
            # cv2.imshow('11', frame)
            # cv2.waitKey(1)
            ret, frame = self.stream.read()

        self.frames = frames

        self.stream.release()
        cv2.destroyAllWindows()

    def add_user_head_feature_(self, frame):
        feature = Face_pose.face_feasture.run(frame)
        if feature is not None:
            feature = feature.astype(np.float16)
            feature = feature.tostring()
            # 存储人脸特征到数据库
            add_user_head_feature(
                User_head_feature_info(user_type=self.face_video_info.user_type, user_id=self.face_video_info.user_id,
                                       head_feature=feature))

    def generate_frame(self):
        """Video streaming generator function."""
        frames = self.run()
        try:
            while True:
                frame = frames.__next__()
                if frame is not None:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                else:
                    break
        except Exception:
            self.add_user_head_feature_(self.frames[0])
            self.add_user_head_feature_(self.frames[1])
            self.add_user_head_feature_(self.frames[4])
            # 存储图片到数据库
            for frame in self.frames:
                byte_frame = cv2.imencode('.jpg', frame)[1].tobytes()
                add_user_head_img(
                    User_head_image_info(user_type=self.face_video_info.user_type, user_id=self.face_video_info.user_id,
                                         image=byte_frame))
            end_frame = cv2.imread('resources/info_record_succeed.jpg')
            end_frame = cv2.imencode('.jpg', end_frame)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + end_frame + b'\r\n')

    def video_generate(self):
        if self.stream.isOpened():
            return StreamingResponse(self.generate_frame(),
                                     media_type='multipart/x-mixed-replace; boundary=frame')
        else:
            def file():
                with open('resources/video_not_open.jpg', mode='rb') as f:
                    yield from f

            return StreamingResponse(file(), media_type='image/jpg')
