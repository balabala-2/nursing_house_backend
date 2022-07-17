from sqlalchemy import Column, String, Date, Integer, BINARY, Text
from dao.config import base


class Interactive(base):
    """
    老人和义工的交互信息
    """
    __tablename__ = 'interactive'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 老人id
    elderly_id = Column(Integer)
    # 义工id
    volunteer_id = Column(Integer)
    # 图片
    img = Column(BINARY)
    # 交谈的文本
    text = Column(String)
    # 日期
    create_time = Column(Date)

class Invade(base):
    """
    入侵到非法区域的信息
    """
    __tablename__ = 'invade'
    # id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 图片
    img = Column(BINARY)
    # 日期
    create_time = Column(Date)

class Fall(base):
    """
    老人摔倒的信息
    """
    __tablename__ = 'fall'
    # id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 图片
    img = Column(BINARY)
    # 日期
    create_time = Column(Date)

class Emotion(base):
    """
    老人情感分析的信息
    """
    __tablename__ = 'emotion'
    # id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 哪个爷笑了
    elderly_id = Column(Integer)
    # 情感类别
    emotion_type = Column(String)
    # 图片
    img = Column(BINARY)
    # 日期
    create_time = Column(Date)

