from fastapi import APIRouter


router = APIRouter()
@router.post("/auth/register" , response_model="")
def registrar_user ():
    pass

@router.post("/auth/login" , response_model="")
def login_user():
    pass