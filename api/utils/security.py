from models.user_model import UserCreate
from dotenv import load_dotenv
from os import getenv
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import jwt

load_dotenv()
ALGORITHM = getenv("ALGORITHM")
SECRET_KEY = getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
# VARIAVEL SERA USADA EM ROTAS PROTEGIDAS 

def criar_hash_senha(senha : str) -> str:
    return pwd_context.hash(senha)

def verificar_senha (senha_padrao : str, senha_hash : str) -> bool:
    return pwd_context.verify(senha_padrao, senha_hash)


def criar_JWT_token (subject: str | int) -> str:
    expiracao = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub" : str(subject),
        "exp" : expiracao,
        "iat" : datetime.now()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_JWT_token (token : str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
    
def retornar_current_user (token : str = Depends(oauth2_scheme)) -> str:
    payload = decodificar_JWT_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload["sub"]