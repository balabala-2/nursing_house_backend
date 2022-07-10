import datetime

from pydantic import BaseModel


# 定义前端传给后端的数据格式

class Login_info(BaseModel):
    """
    基本信息
    login_type: 登录类型
    username: 用户名
    password: 密码
    tel: 电话号码
    """
    login_type: str
    username: str = ''
    password: str = ''
    tel: str = ''


class Register_info(BaseModel):
    """
    基本信息
    username: 用户名
    password: 密码
    tel: 电话号码
    """
    username: str
    password: str
    tel: int


class Manager_info(BaseModel):
    username: str
    name: str = ''
    gender: int = 1
    tel: str
    password: str
    face_feature: str = ''
    entry_time: datetime.date
    resignation_time: datetime.date = None


class Elderly_info(BaseModel):
    """
    老年人信息
    """
    id: int
    name: str
    gender: int
    tel: str
    id_card: str
    birthday: datetime.date
    in_time: datetime.date
    out_time: datetime.date
    face_feature: str
    room_number: str
    guardian_name: str
    guardian_tel: str
    guardian_relation: str
    remarks: str
    create_manager_id: int


class Volunteer_info(BaseModel):
    id: int
    name: str
    gender: int
    tel: str
    education: str
    face_feature: str
    remarks: str
    create_manager_id: int
    entry_time: datetime.date
    resignation_time: datetime.date


class Staff_info(BaseModel):
    id: int
    name: str
    gender: int
    tel: str
    education: str
    face_feature: str
    occupation: str
    wages: int
    remarks: str
    create_manager_id: int
    entry_time: datetime.date
    resignation_time: datetime.date
