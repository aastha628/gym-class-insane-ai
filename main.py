from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from utils.auth import AuthHandler
from routes import views, manager, member, gym_class

app = FastAPI()
auth_handler = AuthHandler()

app.include_router(manager.router, prefix="/api/manager")
app.include_router(member.router, prefix="/api/member")
app.include_router(gym_class.router, prefix="/api/gym-class")
app.include_router(views.router)

app.mount("/", StaticFiles(directory="public"), name="public")
