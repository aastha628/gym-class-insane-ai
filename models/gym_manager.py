from pydantic import BaseModel
from typing import Union


class GymManager(BaseModel):
    id: Union[int, None] = None
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str
