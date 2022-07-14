import datetime

from DAO import user_operation
from schemas.request import Login_info, Register_info, Manager_info
from schemas.response import Base_response
from utils.tokens import create_access_token


def handle_login(login_info: Login_info):
    token, state, msg = "", 0, ""
    if login_info.login_type == "password":
        # 用户名密码登录
        state, msg, manager = user_operation.query_manager_pwd(login_info.username, login_info.password)
    else:
        # 手机验证码登录，发送过来的验证码在前端判断过了，因此是正确的，只需要对应用户
        state, msg, manager = user_operation.query_manager_tel(login_info.tel)

    if state == 1:
        token = create_access_token(manager)
    return Base_response(state=state, msg=msg, token=token)


def handle_register(register_info: Register_info):
    manager_info = register_info.dict()
    manager_info['entry_time'] = datetime.date.today()
    state, msg, manager = user_operation.add_manager(Manager_info(**manager_info))
    token = ""
    if state:
        token = create_access_token(manager)
    return Base_response(state=state, msg=msg, token=token)
