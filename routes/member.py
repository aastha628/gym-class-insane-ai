from fastapi import APIRouter, Response, Depends
from utils.auth import AuthHandler
from models.gym_member import GymMembers as GymMemberModel
from models.gym_member import UpdateMember
from controllers.gym_member import GymMember

router = APIRouter(dependencies=[Depends(AuthHandler().auth_wrapper)])


@router.get("/details")
def get_members_and_membership_type(res: Response):
    return GymMember().get_members_details(res)


@router.post("/")
def create_gym_member(member: GymMemberModel, res: Response):
    return GymMember().create_member(member, res)


@router.delete("/{id}")
def delete_member(id, res: Response):
    return GymMember().delete_member(id, res)


@router.patch("/{id}")
def update_member(id, member: UpdateMember, res: Response):
    return GymMember().update_member(id, member, res)
