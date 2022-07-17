from datetime import datetime

from dao import user_operation
from schemas.request import Elderly_info
from schemas.response import Base_response, Elderly_response, Elderly_ages, Guardian_relation, Elderly_names


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


def handle_update_elderly_info(elderly_info: Elderly_info):
    """
    修改老人信息
    :param id: elderly_info:
    :return:
    """
    state, msg = user_operation.update_elderly(elderly_info)
    return Base_response(state=state, msg=msg)


def handle_all_elderly_ages():
    state, msg, results = user_operation.query_all_elderly_info()
    sixty_seventy = 0
    seventy_eighty = 0
    eighty_ninety = 0
    ninety_hundred = 0
    over_hundred = 0
    currentYear = datetime.now().year
    elderly_num = 0
    for elder in results:
        if elder.out_time is None:
            elderly_num += 1
        sub = currentYear - elder.birthday.year
        if sub >= 60 and sub < 70:
            sixty_seventy += 1
        elif sub >= 70 and sub < 80:
            seventy_eighty += 1
        elif sub >= 80 and sub < 90:
            eighty_ninety += 1
        elif sub >= 90 and sub < 100:
            ninety_hundred += 1
        elif sub >= 100:
            over_hundred += 1
    return Elderly_ages(state=state, msg=msg, sixty_seventy=sixty_seventy, seventy_eighty=seventy_eighty,
                        eighty_ninety=eighty_ninety, ninety_hundred=ninety_hundred, over_hundred=over_hundred,
                        elderly_num=elderly_num)


def handle_all_elderly_relation():
    state, msg, results = user_operation.query_all_elderly_info()
    print(results)
    son = 0
    daughter = 0
    grandson = 0
    granddaughter = 0
    other = 0
    guardian_num = 0
    for elder in results:
        # if elder.out_time is None:
        guardian_num += 1
        relation = elder.guardian_relation
        print(relation)
        if relation == "选项1":
            son += 1
        elif relation == "选项2":
            daughter += 1
        elif relation == "选项3":
            grandson += 1
        elif relation == "选项4":
            granddaughter += 1
        elif relation == "选项5":
            other += 1
    return Guardian_relation(state=state, msg=msg, son=son, daughter=daughter, grandson=grandson,
                             granddaughter=granddaughter, other=other, guardian_num=guardian_num)


def handle_all_elderly_names():
    state, msg, result = user_operation.query_all_elderly_info()
    ids = []
    names = []
    for elder in result:
        ids.append(elder.id)
        names.append(elder.name)
    return Elderly_names(state=state, msg=msg, ids=ids, names=names)
