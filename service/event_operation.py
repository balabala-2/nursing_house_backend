from dao.scene_operation import *
from fastapi.responses import StreamingResponse

def get_img_by_id(event_type, event_id):
    img = get_event_img(event_type=event_type, event_id=event_id)
    return StreamingResponse(iter([img]), media_type='image/jpg')


def handle_query_emotion():
    # 查找所有的情感信息: 查情感数据库,
    state, msg, results = query_emotion()

    return state, msg, results

def handle_query_invade():
    # 查找所有的入侵信息
    state, msg, results = query_invade()

    return state, msg, results

def handle_query_interactive():
    state, msg, results = query_interactive()
    return state, msg, results

def get_single_elderly_emotion(elderly_id):
    state, msg, results = query_emotion_by_id(elderly_id)
    return state, msg, results

def handle_query_fall():
    state, msg, results = query_fall()
    return state, msg, results