from DAO import user_operation
from schemas.request import Staff_info
from schemas.response import Staff_response, Base_response


def handle_query_all_staff_info():
    """
    查询所有员工的信息
    """
    state, msg, results = user_operation.query_all_staff_info()
    return Staff_response(state=state, msg=msg, staff_info=results)


def handle_add_staff_info(staff_info: Staff_info):
    """
    添加员工信息
    """
    state, msg = user_operation.add_staff(staff_info)
    return Base_response(state=state, msg=msg)

def handle_del_staff_info(staff_id):
    """
    删除义工信息
    :param id:
    :return:
    """
    state, msg = user_operation.delete_volunteer(staff_id)
    return Base_response(state=state, msg=msg)