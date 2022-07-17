from pydantic import BaseModel
from schemas.request import Elderly_info, Volunteer_info, Staff_info
from typing import List
import datetime

class Base_response(BaseModel):
    state: int
    msg: str
    token: str = ''
    manager_id: int = -1

class Manager_response(BaseModel):
    state: int
    msg: str

class Manager_msg_response(BaseModel):
    state: int
    msg: str
    username: str
    name: str
    tel: str
    entry_time: datetime.date

class Elderly_response(Base_response):
    elderly_info: List[Elderly_info]

class Elderly_ages(BaseModel):
    state: int
    msg: str
    sixty_seventy: int
    seventy_eighty: int
    eighty_ninety: int
    ninety_hundred: int
    over_hundred: int
    elderly_num: int

class Guardian_relation(BaseModel):
    state: int
    msg: str
    son: int
    daughter: int
    grandson: int
    granddaughter: int
    other: int
    guardian_num: int

class Entry_resignation(Base_response):
    entry_num_info: List[int]
    resignation_num_info: List[int]

class Volunteer_response(Base_response):
    volunteer_info: List[Volunteer_info]

class Staff_response(Base_response):
    staff_info: List[Staff_info]

class Elderly_emotion(BaseModel):
    id: int
    name: str
    emotion_type: str
    create_time: datetime.date


class Elderly_fall(BaseModel):
    id: int
    create_time: datetime.date

#老人义工交互
class Elderly_interactive(BaseModel):
    id: int
    elderly_name: str
    volunteer_name: str
    text: str
    create_time: datetime.date = None

#入侵
class Invade_event(BaseModel):
    id: int
    create_time: datetime.date

class Elderly_names(Manager_response):
    ids: List[int]
    names: List[str]
