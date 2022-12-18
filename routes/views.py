from fastapi import APIRouter
from starlette.responses import FileResponse

router = APIRouter()


@router.get("/manager/register")
def manager_register_page():
    return FileResponse("public/manager/register.html")

@router.get("/manager/login")
def manager_login_page():
    return FileResponse("public/manager/login.html")

@router.get("/manager")
def manager_dashboard():
    return FileResponse("public/manager/dashboard.html")

@router.get("/")
def getHomePage():
    return FileResponse("public/index.html")
