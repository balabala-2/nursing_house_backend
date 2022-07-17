import dlib
import numpy as np
from algorithm.deepface.detectors import FaceDetector


class Face_feature():
    detector_backend = 'ssd'
    detector = FaceDetector.build_model(detector_backend)
    face_detector = FaceDetector.build_model(detector_backend)

    # Dlib 正向人脸检测器
    detector = dlib.get_frontal_face_detector()
    # Dlib 人脸 landmark 特征点检测器
    predictor = dlib.shape_predictor('algorithm/weights/dlib_weights/shape_predictor_68_face_landmarks.dat')
    # Dlib Resnet 人脸识别模型，提取 128D 的特征矢量
    face_reco_model = dlib.face_recognition_model_v1("algorithm/weights/dlib_weights/dlib_face_recognition_resnet_model_v1.dat")

    def __init__(self) -> None:
        pass
    
    def get_128d_features(self, frame):
        """获得图像的128D特征
        Args:
            frames (_type_): cv.imread()
        Returns:
            _type_: _description_
        """
        faces = FaceDetector.detect_faces(Face_feature.face_detector, Face_feature.detector_backend, frame, align = False)
        if len(faces) != 0:
            x, y, w, h = faces[0][1]
            shape = Face_feature.predictor(frame, dlib.rectangle(x, y, x + w, y + h))
            face_descriptor = Face_feature.face_reco_model.compute_face_descriptor(frame, shape)
            return np.array(face_descriptor)
        else:
            return None
    
    def run(self, frame):
        """脸部特征提取

        Args:
            frames (_type_): _description_

        Returns:
            _type_: ndarray 128D
        """
        features = self.get_128d_features(frame)
        return features

        