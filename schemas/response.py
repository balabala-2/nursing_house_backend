from pydantic import BaseModel
from schemas.request import Elderly_info, Volunteer_info, Staff_info
from typing import List

class Base_response(BaseModel):
    state: int
    msg: str
    token: str = ''


class Elderly_response(Base_response):
    elderly_info: List[Elderly_info]

class Volunteer_response(Base_response):
    volunteer_info: List[Volunteer_info]

class Staff_response(Base_response):
    staff_info: List[Staff_info]