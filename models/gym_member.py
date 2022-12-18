from pydantic import BaseModel
from typing import Union
from enum import Enum


class MembershipType(int, Enum):
    basic = 1
    medium = 2
    premium = 3


class GymMembers(BaseModel):
    id: Union[int, None] = None
    name: str
    email: str
    contact: str
    gym_class: Union[str, None] = None
    membership_type: MembershipType

    class config:
        use_enum_values = True
        
class UpdateMember(BaseModel):
    name : Union[str,None]=None
    contact : Union[str,None]=None
    gym_class: Union[str, None] = None
    membership_type: Union[MembershipType,None]=None
    
    class config:
        use_enum_values=True
    
