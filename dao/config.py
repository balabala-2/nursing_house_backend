from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

engine = create_engine("sqlite:///data.db", connect_args={"check_same_thread": False})

Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话类
session = Session_class()  # 生成session实例