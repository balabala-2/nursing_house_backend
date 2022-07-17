import datetime

from dao.config import session
from dao.table.scene import Invade, Fall, Emotion, Interactive
from dao.table.user import Elderly, Volunteer
from schemas.other import Invade_info, Fall_info, Emotion_info, Interactive_info
from schemas.response import Elderly_emotion, Elderly_fall, Elderly_interactive, Invade_event
from collections import Counter

def add_scene(info, table):
    try:
        scene = table(**info.dict())
        session.add(scene)
        session.commit()

        return 1, "添加成功"
    except Exception as e:
        return 0, f"添加失败: {e}"


def add_invade(invade_info: Invade_info):
    return add_scene(invade_info, Invade)


def add_fall(fall_info: Fall_info):
    return add_scene(fall_info, Fall)


def add_emotion(emotion_info: Emotion_info):
    return add_scene(emotion_info, Emotion)


def add_interactive(interactivate_info: Interactive_info):
    return add_scene(interactivate_info, Interactive)


def query_emotion():
    try:
        items = session.query(Emotion, Elderly).filter(Emotion.elderly_id == Elderly.id).all()
        results = []
        for emotion, elderly in items:
            results.append(Elderly_emotion(id=elderly.id, name=elderly.name, emotion_type=emotion.emotion_type,
                                           create_time=emotion.create_time))
        return 1, "查询成功", results
    except Exception as e:
        print(e)
        return 0, "查询失败", None


def query_emotion_by_id(elderly_id):
    try:
        items = session.query(Emotion).filter(Emotion.elderly_id == elderly_id).order_by(Emotion.create_time).all()
        results = dict(Counter([item.create_time for item in items]))
        dates = [0 for _ in range(7)]
        for result in results.keys():
            dates[6 - (datetime.date.today() - result).days] += results[result]
        return 1, "查询成功", dates
    except Exception as e:
        print(e)
        return 0, "查询失败", None


def query_invade():
    try:
        items = session.query(Invade).all()
        results = []
        for item in items:
            results.append(Invade_event(id=item.id, create_time=item.create_time))
        return 1, "查询成功", results
    except Exception as e:
        print(e)
        return 0, "查询失败", None


def query_interactive():
    try:
        items = session.query(Interactive).all()
        results = []
        for item in items:
            elderly_name = '陌生人'
            volunteer_name = '陌生人'
            if item.elderly_id != -1:
                elderly_name = session.query(Elderly).filter_by(id=item.elderly_id).first().name
            if item.volunteer_id != -1:
                volunteer_name = session.query(Volunteer).filter_by(id=item.volunteer_id).first().name
            results.append(Elderly_interactive(id=item.id, elderly_name=elderly_name, volunteer_name=volunteer_name,
                                               create_time=item.create_time, text=item.text))
        return 1, "查询成功", results
    except Exception as e:
        print(e)
        return 0, "查询失败", None


def query_fall():
    try:
        items = session.query(Fall).all()
        results = []
        for item in items:
            results.append(Elderly_fall(id=item.id, create_time=item.create_time))
        return 1, "查询成功", results
    except Exception as e:
        print(e)
        return 0, "查询失败", None


def get_event_img(event_type, event_id):
    table = None
    if event_type == 'fall':
        table = Fall
    elif event_type == 'invade':
        table = Invade
    elif event_type == 'interactive':
        table = Interactive
    elif event_type == 'emotion':
        table = Emotion
    if table is not None:
        info = session.query(table).filter_by(id=event_id).first()
        if info is not None:
            return info.img
    return None
