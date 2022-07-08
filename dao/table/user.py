from sqlalchemy import Column, String, Date, Integer, BOOLEAN, BINARY

from dao.config import base


class Manager(base):
    """
    系统管理员信息
    """
    __tablename__ = 'manager'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 用户名
    username = Column(String, unique=True)
    # 姓名
    name = Column(String, default="")
    # 性别
    gender = Column(BOOLEAN, default=True)
    # 电话
    tel = Column(String, unique=True)
    # 密码
    password = Column(String, nullable=False)
    # 录入脸部特征
    face_feature = Column(String, default="")

    # 入职时间
    entry_time = Column(Date)
    # 离职时间
    resignation_time = Column(Date, default=None)


class Elderly(base):
    """
    老年人信息
    """
    __tablename__ = 'elderly'
    # id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 姓名
    name = Column(String)
    # 性别: m, w, -
    gender = Column(BOOLEAN)
    # 电话
    tel = Column(String, unique=True)
    # 身份证
    id_card = Column(String)
    # 生日
    birthday = Column(Date)
    # 入院日期
    in_time = Column(Date)
    # 出院日期
    out_time = Column(Date, default=None)
    # 录入脸部特征
    face_feature = Column(String)
    # 房间号
    room_number = Column(String)

    # 监护人姓名，电话，与老人的关系
    guardian_name = Column(String)
    guardian_tel = Column(String)
    guardian_relation = Column(String)

    # 备注
    remarks = Column(String)

    # 负责该老人入院的管理员id
    create_manager_id = Column(Integer)


class Volunteer(base):
    """
    义工信息
    """
    __tablename__ = 'volunteer'
    # id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 姓名
    name = Column(String)
    # 性别: m, w, -
    gender = Column(BOOLEAN)
    # 电话
    tel = Column(String, unique=True)
    # 学历
    education = Column(String)
    # 录入脸部特征
    face_feature = Column(String)

    # 备注
    remarks = Column(String)
    # 负责录入该义工信息的管理员id
    create_manager_id = Column(Integer)

    # 入职时间
    entry_time = Column(Date)
    # 离职时间
    resignation_time = Column(Date, default=None)


class Staff(base):
    """
    义工信息
    """
    __tablename__ = 'staff'
    # id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 姓名
    name = Column(String)
    # 性别: m, w, -
    gender = Column(BOOLEAN)
    # 电话
    tel = Column(String, unique=True)
    # 学历
    education = Column(String)
    # 录入脸部特征
    face_feature = Column(String)

    # 职务(清洁工，食堂大妈)
    occupation = Column(String)

    # 工资
    wages = Column(Integer)

    # 备注
    remarks = Column(String)
    # 负责录入该员工信息的管理员id
    create_manager_id = Column(Integer)

    # 入职时间
    entry_time = Column(Date)
    # 离职时间
    resignation_time = Column(Date, default=None)


class User_head_feature(base):
    """
    人物的脸部特征数据
    """
    __tablename__ = 'user_head_feature'
    # id
    id = Column(Integer, primary_key=True, autoincrement=True)

    # 人员类型：manager, elderly, volunteer, staff
    user_type = Column(String)
    # 人员对应的id
    user_id = Column(Integer)
    # 人脸特征：ndarray -> '.npy' byte
    head_feature = Column(BINARY)


class User_head_image(base):
    """
    人物的头像数据
    """
    __tablename__ = 'user_head_image'
    # id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # user_head_feature id
    head_feature_id = Column(Integer)
    # image -> byte
    image = Column(BINARY)
