import torch
from algorithm.deepface import DeepFace
import dlib
from algorithm.deepface.detectors import FaceDetector

video_width = 640
video_height = 480

fall_detection_url = 'resources/fall_video.mp4'
emotion_detection_url = 'resources/emotion_video.mp4'
invade_detection_url = 'resources/invade_video.mp4'
interactive_detection_url = 'resources/interactive_video.mp4'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

facepose_weights = {
    'model': 'algorithm/weights/facepose_weights/checkpoint.pth.tar',
    'caffemodel': "algorithm/weights/facepose_weights/Widerface-RetinaFace.caffemodel",
    'deploy': 'algorithm/weights/facepose_weights/deploy.prototxt'
}

invade_weights = {
    'prototxt': 'algorithm/weights/invade_weights/MobileNetSSD_deploy.prototxt',
    'model': 'algorithm/weights/invade_weights/MobileNetSSD_deploy.caffemodel'
}

emotions_weights = {
    'model': 'algorithm/weights/emotion_weights/emotion_model.hdf5',
    'face_cascade': 'algorithm/weights/emotion_weights/haarcascade_frontalface_default.xml'
}

fall_weights = {
    'model': 'algorithm/weights/fall_weights/best.pt',
    'data': 'algorithm/weights/fall_weights/fall_down.yaml'
}

detector_backend = 'ssd'
# 人脸识别模型
face_detector = FaceDetector.build_model(detector_backend)
# 情绪识别模型
emotion_model = DeepFace.build_model('Emotion')
# Dlib 人脸 landmark 特征点检测器 / Get face landmarks
face_landmarks_extractor = dlib.shape_predictor('algorithm/weights/dlib_weights/shape_predictor_68_face_landmarks.dat')
# Dlib Resnet 人脸识别模型, 提取 128D 的特征矢量
face_feature_extractor = dlib.face_recognition_model_v1("algorithm/weights/dlib_weights/dlib_face_recognition_resnet_model_v1.dat")