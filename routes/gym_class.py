from fastapi import APIRouter, Response, Depends
from utils.auth import AuthHandler
from models.gym_class import GymClass as GymClassModel
from models.gym_class import UpdateClass
from controllers.gym_class import GymClass


router = APIRouter(dependencies=[Depends(AuthHandler().auth_wrapper)])


@router.get("/details")
def get_details(res: Response):
    return GymClass().get_all_gym_classes(res)


@router.get("/{class_id}/members")
def get_all_members(class_id, res: Response):
    return GymClass().get_all_members(class_id, res)


@router.post("/")
def create_gym_class(gym_class: GymClassModel, res: Response):
    return GymClass().create_gym_class(gym_class, res)


@router.delete("/{id}")
def delete_gym_class(id, res: Response):
    return GymClass().delete_gym_class(id, res)


@router.patch("/{id}")
def update_gym_class(id, gym_class: UpdateClass, res: Response):
    return GymClass().update_gym_class(id, gym_class, res)
