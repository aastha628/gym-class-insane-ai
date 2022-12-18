from fastapi import APIRouter, Response
from starlette.responses import FileResponse
from models.gym_manager import GymManager, LoginRequest
from controllers.gym_manager import GymManager as GM_Controller

router = APIRouter()


@router.post("/register")
def register(manager: GymManager, res: Response):
    return GM_Controller().register_manager(manager, res)


@router.post("/login")
def login(manager: LoginRequest, res: Response):
    return GM_Controller().login_manager(manager, res)


@router.get("/")
def get_manager():
    return {"hello": "manager here"}
