import datetime

import numpy as np
import torch
import cv2
from fastapi.responses import StreamingResponse

from algorithm.fall_detection.models.common import DetectMultiBackend
from algorithm.fall_detection.utils.general import (check_img_size, non_max_suppression, scale_coords)
from algorithm.fall_detection.utils.plots import Annotator, colors
from algorithm.fall_detection.utils.augmentations import letterbox
from algorithm.utils.global_variable import device, fall_weights, fall_detection_url, video_width, video_height
from dao.scene_operation import add_fall
from schemas.other import Fall_info
import requests
def send_wechat(msg):
    token = 'a3f6f1785ace45679917b13bcebe6f53'  # 前边复制到那个token
    title = '有事件发生！！！'
    content = msg
    template = 'markdown'
    url = f"https://www.pushplus.plus/send?token={token}&title={title}&content={content}&template={template}"
    requests.get(url=url)

class Fall_detection:
    def __init__(self):
        self.stream = cv2.VideoCapture(fall_detection_url)
        self.stream.set(3, video_width)
        self.stream.set(4, video_height)

        self.fall_list = []

    def run(self):
        model = DetectMultiBackend(fall_weights['model'], device=device, dnn=True, data=fall_weights['data'], fp16=True)
        stride, names, pt = model.stride, model.names, model.pt
        img_size = check_img_size((384, 384), s=stride)
        model.warmup(imgsz=(1, 3, *img_size))
        fall_frame = None
        fall_pred = 0.0

        while True:
            ret, frame = self.stream.read()
            if not ret:
                break
            frame_copy = frame.copy()
            img = cv2.resize(frame_copy, img_size)
            img = letterbox(img, img_size, stride=stride, auto=pt)[0]
            img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
            img = np.ascontiguousarray(img)

            img = torch.from_numpy(img).to(device).float() / 255
            # Convert
            if len(img.shape) == 3:
                img = img[None]  # expand for batch dim
            pred = model(img, augment=False, visualize=False)
            pred = non_max_suppression(pred, 0.25, 0.45, None, True, max_det=1000)

            for i, det in enumerate(pred):
                annotator = Annotator(frame, line_width=3, example=str(names))
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()
                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        c = int(cls)  # integer class
                        label = f'{names[c]} {conf:.2f}'
                        if conf > 0.7:
                            annotator.box_label(xyxy, label, color=colors(c, True))
                            self.fall_list.append(1)
                        if conf > fall_pred:
                            fall_pred = conf
                            fall_frame = annotator.result()
            new_img = annotator.result()

            if len(self.fall_list) > 50:
                if np.array(self.fall_list).sum() > 40 and fall_frame is not None:
                    add_fall(Fall_info(img=cv2.imencode('.jpg', fall_frame)[1].tobytes()))
                    send_wechat(str(datetime.datetime.today()) + ': 检测到老人摔倒，请前往客户端查看')
                self.fall_list = []
                fall_pred = 0.0
                fall_frame = None

            yield cv2.imencode('.jpg', new_img)[1].tobytes()

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
            pass

    def video_generate(self):
        if self.stream.isOpened():
            return StreamingResponse(self.generate_frame(),
                                    media_type='multipart/x-mixed-replace; boundary=frame')
        else:
            def file():
                with open('resources/video_not_open.jpg', mode='rb') as f:
                    yield from f
            return StreamingResponse(file(), media_type='image/jpg')
