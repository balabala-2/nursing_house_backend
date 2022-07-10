from dao import user_operation
from schemas.request import Elderly_info
from schemas.response import Base_response, Elderly_response


def handle_query_all_elderly_info():
    """
    查询所有老人的信息
    :return:
    """
    state, msg, results = user_operation.query_all_elderly_info()
    return Elderly_response(state=state, msg=msg, elderly_info=results)


def handle_add_elderly_info(elderly_info: Elderly_info):
    """
    添加老人信息
    :param elderly_info:
    :return:
    """
    state, msg = user_operation.add_elderly(elderly_info)
    return Base_response(state=state, msg=msg)


def handle_del_elderly_info(elderly_id):
    """
    删除老人信息
    :param id:
    :return:
    """
    state, msg = user_operation.delete_elderly(elderly_id)
    return Base_response(state=state, msg=msg)

def handle_update_elderly_info (elderly_info: Elderly_info):
    """
    修改老人信息
    :param id: elderly_info:
    :return:
    """
    state, msg = user_operation.update_elderly(elderly_info)
    return Base_response(state=state, msg=msg)