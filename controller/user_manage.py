from fastapi import APIRouter

from schemas.request import Elderly_info, Staff_info, Volunteer_info, Manager_info, Manager_info_to_update, Manager_password_to_update
from service import elderly_operation, staff_operation, volunteer_operation, manager_operation
router = APIRouter()

"""
----------------------------------------------------------------------
信息查询
----------------------------------------------------------------------
"""


@router.post('/api/elderly_info', name='查询老人信息')
def get_elderly_info():
    response = elderly_operation.handle_query_all_elderly_info()
    return response


@router.post('/api/staff_info', name='查询员工信息')
def get_staff_info():
    response = staff_operation.handle_query_all_staff_info()
    return response


@router.post('/api/volunteer_info', name='查询义工信息')
def get_volunteer_info():
    response = volunteer_operation.handle_query_all_volunteer_info()
    return response


"""
----------------------------------------------------------------------
信息添加
----------------------------------------------------------------------
"""


@router.post('/api/add_elderly_info', name='添加老人信息')
def add_elderly_info(elderly_info: Elderly_info):
    response = elderly_operation.handle_add_elderly_info(elderly_info)
    return response


@router.post('/api/add_staff_info', name='添加员工信息')
def add_elderly_info(staff_info: Staff_info):
    response = staff_operation.handle_add_staff_info(staff_info)
    return response


@router.post('/api/add_volunteer_info', name='添加义工信息')
def add_elderly_info(volunteer_info: Volunteer_info):
    response = volunteer_operation.handle_add_volunteer_info(volunteer_info)
    return response


"""
----------------------------------------------------------------------
信息删除
----------------------------------------------------------------------
"""


@router.post('/api/del_volunteer_info/{volunteer_id}', name='删除义工信息')
def del_volunteer_info(volunteer_id: int):
    response = volunteer_operation.handle_del_volunteer_info(volunteer_id)
    return response


@router.post('/api/del_elderly_info/{elderly_id}', name='删除老人信息')
def del_elderly_info(elderly_id: int):
    response = elderly_operation.handle_del_elderly_info(elderly_id)
    return response


@router.post('/api/del_staff_info/{staff_id}', name='删除员工信息')
def del_staff_info(staff_id: int):
    response = staff_operation.handle_del_staff_info(staff_id)
    return response


"""
----------------------------------------------------------------------
信息修改
----------------------------------------------------------------------
"""
# TODO

@router.post('/api/update_volunteer_info', name='修改义工信息')
def update_volunteer_info(volunteer_info: Volunteer_info):
    response = volunteer_operation.handle_update_volunteer_info(volunteer_info)
    return response


@router.post('/api/update_elderly_info', name='修改老人信息')
def update_elderly_info(elderly_info: Elderly_info):
    """
    根据id修改老年人信息
    """
    response = elderly_operation.handle_update_elderly_info(elderly_info)
    return response


@router.post('/api/update_staff_info', name='修改员工信息')
def update_staff_info(staff_info: Staff_info):
    response = staff_operation.handle_update_staff_info(staff_info)
    return response

@router.post('/api/update_manager_info', name='修改管理员信息')
def update_manager_info(manager_info: Manager_info_to_update):
    response = manager_operation.handle_info_update(manager_info)
    return response

@router.post('/api/update_manager_password', name='修改管理员密码')
def update_manager_password(manager_info: Manager_password_to_update):
    response = manager_operation.handle_password_update(manager_info)
    return response

@router.get('/api/get_manager_info/{manager_id}', name='查询管理员信息')
def get_manager_info(manager_id: int):
    response = manager_operation.handle_manager_msg_query(manager_id)
    return response