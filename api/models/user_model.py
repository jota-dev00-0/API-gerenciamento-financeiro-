from pydantic import BaseModel , EmailStr, SecretStr

class UserBase(BaseModel):
    nome : str
    email : EmailStr
    
class UserCreate(UserBase):
    senha : SecretStr
    
class UserDB(UserBase):
    id : int
    senha_hash : str
    
    class Config:
        orm_mode : True
        
        
class TokenResponse(BaseModel):
    access_token: str
    token_type: str