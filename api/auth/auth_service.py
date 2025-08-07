from fastapi.security import OAuth2PasswordBearer
from core.database import get_database_connection, get_user_by_email_db, create_user_db
from utils.security import criar_hash_senha, criar_JWT_token
from models.user_model import UserCreate, UserDB, TokenResponse
from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext
from typing import Optional
from utils.security import criar_hash_senha, verificar_senha, decodificar_JWT_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_user_by_email (email : str) -> Optional[UserDB]:
    return get_user_by_email_db(email)

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    payload = decodificar_JWT_token(token)
    
    if not payload:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido (subject ausente)",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    return user_id

def create_user(nome: str, email: str, senha_hash: str) -> UserDB:
    return create_user_db(nome, email, senha_hash)
    
    
def register_user(user_data : UserCreate) -> UserDB:
    existing_user = get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Email ja cadastrado"
        )  
    
    senha_hash = criar_hash_senha(user_data.senha)
    
    novo_usuario = create_user(
        nome=user_data.nome,
        email=user_data.email,
        senha=senha_hash
    )
    
    return novo_usuario




def login_user_service(credentials : UserCreate) -> TokenResponse:
    usuario = get_user_by_email(credentials.email)
    
    if not usuario or not verificar_senha(credentials.senha, usuario.senha_hash):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
            )
    
    acess_token = criar_JWT_token(subject=str(usuario.id))
    
    return TokenResponse(
        acess_token=acess_token,
        token_type="bearer"
    )
    
    