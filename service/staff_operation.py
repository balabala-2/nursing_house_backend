from dao import user_operation
from schemas.request import Staff_info
from schemas.response import Staff_response, Base_response, Entry_resignation


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
    state, msg = user_operation.delete_staff(staff_id)
    return Base_response(state=state, msg=msg)

def handle_update_staff_info (staff_info: Staff_info):
    """
    更新老人信息
    :return:
    """
    state, msg = user_operation.update_staff(staff_info)
    return Base_response(state=state, msg=msg)

def handle_all_entry_resignation():
    state, msg, results = user_operation.query_all_staff_info()
    entry_list = [0 for _ in range(12)]
    resignation_list = [0 for _ in range(12)]


    for staff in results:
        entry_list[staff.entry_time.month - 1] += 1
        if staff.resignation_time is not None:
            resignation_list[staff.resignation_time.month - 1] += 1
    return Entry_resignation(state=1, msg="查询成功", entry_num_info=entry_list, resignation_num_info=resignation_list)