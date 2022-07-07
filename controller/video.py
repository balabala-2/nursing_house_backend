from fastapi.responses import StreamingResponse
import cv2

from utils.camera import Camera
from fastapi import APIRouter

router = APIRouter()
def generate_frame(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_generate(video_url):
    stream = cv2.VideoCapture(video_url)
    if stream.isOpened():
        return StreamingResponse(generate_frame(Camera(video_url=video_url, stream=stream)),
                                 media_type='multipart/x-mixed-replace; boundary=frame')
    else:
        def file():
            with open('resources/video_not_open.jpg', mode='rb') as f:
                yield from f
        return StreamingResponse(file(), media_type='image/jpg')


@router.get('/api/room_video', response_class=StreamingResponse)
def video():
    return video_generate('-')

@router.get('/api/aisle_video', response_class=StreamingResponse)
def video():
    return video_generate('-')

@router.get('/api/yard_video', response_class=StreamingResponse)
def video():
    return video_generate('-')

@router.get('/api/desk_video', response_class=StreamingResponse)
def video():
    return video_generate('-')

@router.get('/api/face_video', response_class=StreamingResponse)
def video():
    return video_generate('-')
