from pydantic import BaseModel
from typing import Union
from datetime import time

class GymClass(BaseModel):
    id : Union[int,None]=None
    name:str
    instructor:str
    time:time
    capacity:int
    current_member_count:Union[int,None]=None
    
class UpdateClass(BaseModel):
    instructor:Union[str,None]=None
    time:Union[time,None]=None
    capacity:Union[int,None]=None
    current_member_count:Union[int,None]=None