from fastapi import APIRouter

from schemas.request import Login_info, Register_info
from service import manager_operation

router = APIRouter()


# 用户登录
@router.post('/api/login', name='登陆')
def login(login_info: Login_info):
    response = manager_operation.handle_login(login_info)
    return response


# 用户注册
@router.post('/api/register', name='注册')
def register(register_info: Register_info):
    response = manager_operation.handle_register(register_info)
    return response
