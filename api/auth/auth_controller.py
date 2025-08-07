from fastapi import APIRouter
from models.user_model import UserDB, UserCreate
from auth_service import register_user

router = APIRouter()
@router.post("/auth/register" , response_model=UserDB)
async def registrar_user (user_data : UserCreate):
    await register_user(user_data)

@router.post("/auth/login" , response_model="")
async def login_user(credentials : UserCreate):
    await login_user(credentials)