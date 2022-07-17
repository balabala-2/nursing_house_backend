from fastapi.responses import StreamingResponse
import cv2
from algorithm.utils.global_variable import video_height, video_width

class Detection:
    def __init__(self) -> None:
        stream = cv2.VideoCapture(0)
        stream.set(3, video_width)
        stream.set(4, video_height)

        self.stream = stream

    def run(self):
        pass

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