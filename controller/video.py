from fastapi import APIRouter

from service.event_operation import get_img_by_id
from service.video_operation import *

router = APIRouter()


@router.get('/api/room_video', response_class=StreamingResponse, name='情绪检测')
async def video():
    return get_emotion_video()


@router.get('/api/aisle_video', response_class=StreamingResponse, name='摔倒检测')
def video():
    return get_fall_video()


@router.get('/api/yard_video', response_class=StreamingResponse, name='入侵检测')
def video():
    return get_invade_video()


@router.get('/api/desk_video', response_class=StreamingResponse, name="交互检测，应该是义工和老人的交互")
def video():
    return get_interactive_video()


@router.get('/api/face_video/{type_id}', response_class=StreamingResponse, name="人脸录入")
def video(type_id: str):
    info = type_id.split('_')
    return face_image_collect(Face_video_info(user_id=int(info[1]), user_type=info[0]))


@router.get('/api/volunteer_img/{user_id}')
def get_img(user_id: int):
    return get_img_by_id('volunteer', user_id)


@router.get('/api/elderly_img/{user_id}')
def get_img(user_id: int):
    return get_img_by_id('elderly', user_id)


@router.get('/api/staff_img/{user_id}')
def get_img(user_id: int):
    return get_img_by_id('staff', user_id)
