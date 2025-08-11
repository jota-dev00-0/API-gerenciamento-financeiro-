from fastapi import APIRouter
from pydantic import BaseModel
from models.user_model import UserDB, UserCreate, TokenResponse
from auth.auth_service import register_user, login_user_service

router = APIRouter(prefix="/auth", tags=["Authenticate"])

@router.post("/register" ,summary="Registrar um User" ,response_model=UserDB)
async def registrar_user (user_data : UserCreate):
    return await register_user(user_data)

@router.post("/login" ,summary="Validar um User" ,response_model=TokenResponse )
async def login_user(credentials : UserCreate):
    return await login_user_service(credentials)