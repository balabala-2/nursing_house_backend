from pydantic import BaseModel
import datetime

class Interactive_info(BaseModel):
    """
    老人和义工的交互信息
    """
    # 老人id
    elderly_id: int
    # 义工id
    volunteer_id: int
    # 图片
    img: bytes
    # text
    text: str
    # 日期
    create_time: datetime.date = datetime.date.today()

class Invade_info(BaseModel):
    """
    入侵到非法区域的信息
    """
    # 图片
    img: bytes
    # 日期
    create_time: datetime.date = datetime.date.today()

class Fall_info(BaseModel):
    """
    老人摔倒的信息
    """
    # 图片
    img: bytes
    # 日期
    create_time: datetime.date = datetime.date.today()

class Emotion_info(BaseModel):
    """
    老人情感分析的信息
    """
    # 哪个爷笑了
    elderly_id: str
    # 情感类别
    emotion_type: str
    # 图片
    img: bytes
    # 日期
    create_time: datetime.date = datetime.date.today()

class User_head_feature_info(BaseModel):
    user_type: str
    user_id: int
    head_feature: bytes

class User_head_image_info(BaseModel):
    user_type: str
    user_id: int
    image: bytes