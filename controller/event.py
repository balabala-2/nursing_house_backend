from fastapi import APIRouter
from service import elderly_operation, volunteer_operation,staff_operation, event_operation
from service.event_operation import get_img_by_id
router = APIRouter()


"""
----------------------------------------------------------------------
图表统计信息查询
----------------------------------------------------------------------
"""
@router.get('/api/get_elderly_ages', name='get_elderly_ages')
def get_elderly_ages():
    response = elderly_operation.handle_all_elderly_ages()
    return response

@router.get('/api/get_guardian_relation', name='get_elderly_relation')
def get_guardian_relation():
    response = elderly_operation.handle_all_elderly_relation()
    return response

@router.get('/api/get_volunteer_entry_resignation', name='get_volunteer_entry_resignation')
def get_volunteer_entry_resignation():
    response = volunteer_operation.handle_all_entry_resignation()
    return response

@router.get('/api/get_staff_entry_resignation', name='get_staff_entry_resignation')
def get_staff_entry_resignation():
    response = staff_operation.handle_all_entry_resignation()
    return response


"""
----------------------------------------------------------------------
事件查询
----------------------------------------------------------------------
"""

@router.get('/api/get_elder_emotion', name='get_elder_emotion')
def get_elder_emotion():
    response = event_operation.handle_query_emotion()
    return response

@router.get('/api/get_single_elderly_emotion/{elderly_id}')
def get_elderly_emotion(elderly_id):
    response = event_operation.get_single_elderly_emotion(elderly_id)
    return response

@router.get('/api/get_invade_event', name='get_invade_event')
def get_invade_event():
    #入侵
    response = event_operation.handle_query_invade()
    return response

@router.get('/api/get_fall_event', name='get_fall_event')
def get_fall_event():
    response = event_operation.handle_query_fall()
    return response

@router.get('/api/get_interactive_event', name='get_interactive_event')
def get_interactive_event():
    response = event_operation.handle_query_interactive()
    return response

@router.get('/api/emotion_img/{img_id}')
def get_emotion_img(img_id: int):
    return get_img_by_id('emotion', img_id)

@router.get('/api/invade_img/{img_id}')
def get_invade_img(img_id: int):
    return get_img_by_id('invade', img_id)

@router.get('/api/interactive_img/{img_id}')
def get_interactive_img(img_id: int):
    return get_img_by_id('interactive', img_id)

@router.get('/api/fall_img/{img_id}')
def get_fall_img(img_id: int):
    return get_img_by_id('fall', img_id)

@router.get('/api/get_elderly_names', name='get_elderly_names')
def get_elderly_names():
    response = elderly_operation.handle_all_elderly_names()
    return response