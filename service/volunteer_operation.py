from dao import user_operation
from schemas.request import Volunteer_info
from schemas.response import Volunteer_response, Base_response, Entry_resignation


def handle_query_all_volunteer_info():
    """
    查询所有义工的信息
    """
    state, msg, results = user_operation.query_all_volunteer_info()
    return Volunteer_response(state=state, msg=msg, volunteer_info=results)


def handle_add_volunteer_info(volunteer_info: Volunteer_info):
    """
    添加义工信息
    """
    state, msg = user_operation.add_volunteer(volunteer_info)
    return Base_response(state=state, msg=msg)


def handle_del_volunteer_info(volunteer_id):
    """
    删除义工信息
    :param id:
    :return:
    """
    state, msg = user_operation.delete_volunteer(volunteer_id)
    return Base_response(state=state, msg=msg)


def handle_update_volunteer_info(volunteer_info: Volunteer_info):
    """
    修改老人信息
    :param id: elderly_info:
    :return:
    """
    state, msg = user_operation.update_volunteer(volunteer_info)
    return Base_response(state=state, msg=msg)


def handle_all_entry_resignation():
    state, msg, results = user_operation.query_all_volunteer_info()
    entry_list = [0 for _ in range(12)]
    resignation_list = [0 for _ in range(12)]

    for volunteer in results:
        entry_list[volunteer.entry_time.month - 1] += 1
        if volunteer.resignation_time is not None:
            resignation_list[volunteer.resignation_time.month - 1] += 1
    return Entry_resignation(state=1, msg="查询成功", entry_num_info=entry_list, resignation_num_info=resignation_list)
