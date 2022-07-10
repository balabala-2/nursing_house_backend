from dao.config import session
from dao.table.user import *
from schemas.request import Manager_info, Volunteer_info, Elderly_info, Staff_info

"""
----------------------------------------------------------------------
信息修改
----------------------------------------------------------------------
"""
# TODO
def update_item(item_type, item_info):
    """
    修改指定的对象
    :param item_type: 对象类型（如Elderly）
    :param item_id: 对象id（如Elderly_id）
    :return:
    """
    try:
        session.query(item_type).filter(item_type.id == item_info.id).update(item_info.dict())
        # if item:
        #     # 部分更新
        #     update_dict = item_type.dict(exclude_unset=True)
        #     for k, v in update_dict.items():
        #         setattr(item, k, v)
        session.commit()
        session.flush()
        return 1, "修改成功"
    except Exception as e:
        print(e)
        return 0, "修改失败"


def update_volunteer(volunteer_info):
    """
    删除指定义工信息
    """
    return update_item(Volunteer, volunteer_info)


def update_elderly(elderly_info):
    """
    删除指定老人信息
    """
    return update_item(Elderly, elderly_info)

def update_staff(staff_info):
    """
    删除指定老人信息
    """
    return update_item(Staff, staff_info)


"""
----------------------------------------------------------------------
信息添加
----------------------------------------------------------------------
"""


def add_manager(manager_info: Manager_info):
    """
    注册管理员
    需要判断用户名和手机号是否存在
    :param manager_info: 管理员信息
    :return:
    """
    manager = session.query(Manager).filter_by(username=manager_info.username).first()

    if manager is not None:
        return 0, "用户名已存在", None

    manager = session.query(Manager).filter_by(tel=manager_info.tel).first()
    if manager is not None:
        return 0, "该手机号已注册", None

    try:
        manager = Manager(**manager_info.dict())
        session.add(manager)
        session.commit()
        return 1, "注册成功", manager
    except Exception:
        return 0, "注册失败", None


def add_volunteer(volunteer_info: Volunteer_info):
    """
    添加志愿者
    直接添加，无需判断
    :param volunteer_info:
    :return:
    """
    try:
        volunteer = Volunteer(**volunteer_info.dict())
        session.add(volunteer)
        session.commit()

        return 1, "成功添加义工信息"
    except Exception:
        return 0, "添加义工信息失败"


def add_elderly(elderly_info: Elderly_info):
    """
    添加老人信息
    直接添加，无需判断
    :param elderly_info:
    :return:
    """
    try:
        elderly = Elderly(**elderly_info.dict())
        session.add(elderly)
        session.commit()
        return 1, "成功添加老人信息"
    except Exception:
        return 0, "添加老人信息失败"


def add_staff(staff_info: Staff_info):
    """
    添加员工信息
    :param staff_info:
    :return:
    """
    try:
        staff = Staff(**staff_info.dict())
        session.add(staff)
        session.commit()
        return 1, "成功添加员工信息"
    except Exception:
        return 0, "添加员工信息失败"


"""
----------------------------------------------------------------------
信息删除
----------------------------------------------------------------------
"""

def delete_item(item_type, item_id):
    """
    删除指定的对象
    :param item_type: 对象类型（Elderly）
    :param item_id: 对象id（Elderly_id）
    :return:
    """
    try:
        item = session.query(item_type).filter(item_type.id==item_id).first()
        session.delete(item)
        session.commit()

        return 1, "删除成功"
    except Exception:
        return 0, "删除失败"

def delete_volunteer(volunteer_id):
    """
    删除指定义工信息
    """
    return delete_item(Volunteer, volunteer_id)


def delete_elderly(elderly_id):
    """
    删除指定老人信息
    """
    return delete_item(Elderly, elderly_id)

def delete_staff(staff_id):
    """
    删除指定老人信息
    """
    return delete_item(Staff, staff_id)

"""
----------------------------------------------------------------------
信息查询
----------------------------------------------------------------------
"""


def query(query_type, query_type_info):
    """
    查询指定类型的所有信息
    :param query_type: 要查询的类型（Elderly）
    :param query_type_info: 查询的类型的schema（Elderly_info）
    :return:
    """
    try:
        items = session.query(query_type).all()

        results = []
        for item in items:
            item = item.__dict__
            item.pop('_sa_instance_state')
            results.append(query_type_info(**item))
        return 1, "查询成功", results

    except Exception:
        return 0, "查询失败", None


def query_all_elderly_info():
    """
    查询所有老人的信息
    :return:
    """
    return query(Elderly, Elderly_info)


def query_all_volunteer_info():
    """
    查询所有义工信息
    :return:
    """
    return query(Volunteer, Volunteer_info)


def query_all_staff_info():
    """
    查询所有义工信息
    :return:
    """
    return query(Staff, Staff_info)


def query_manager_pwd(username, password):
    """
    用户名密码查询管理员
    :param username: 用户名
    :param password: 密码
    :return:
    """
    manager = session.query(Manager).filter_by(username=username).one()
    if manager is None or manager.password != password:
        return 0, "用户名或密码错误", None
    else:
        return 1, "登陆成功", manager


def query_manager_tel(tel):
    """
    加入验证码登陆
    :param tel:
    :return:
    """
    manager = session.query(Manager).filter(Manager.tel == tel).first()
    if manager is None or manager.tel != tel:
        return 0, "该手机未注册", None
    else:
        return 1, "该手机已注册，可以发送验证码", manager
