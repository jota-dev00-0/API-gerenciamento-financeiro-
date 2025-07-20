from pydantic import BaseModel, field_validator 
from typing import Optional
from datetime import datetime

class Transacao (BaseModel):
    id : int
    valor : float
    tipo : str
    descricao : Optional[str] = None
    data : datetime   
    
    @field_validator("tipo")
    def validador(cls, value):
        tipos_aceitos = {"entrada", "saida"}
        if value.lower() not in tipos_aceitos:
             raise ValueError("O tipo deve ser 'entrada' ou 'saida'")
        return value.lower()
    
class TransacaoCreate (Transacao):
    pass 

class TransacaoUpdate(BaseModel):
    valor: Optional[float] = None
    tipo: Optional[str] = None
    descricao: Optional[str] = None
    data: Optional[datetime] = None