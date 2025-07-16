from fastapi import APIRouter, Query, Response
from service.transacao_service import * 
from typing import Optional
router = APIRouter()

@router.get("transacao")
def get_transacoes(tipo: Optional[str] = Query(None, description="Filtrar por tipo: entrada ou saida")):
    lista_transacao(tipo)
    
@router.get("transacao/{id}")
def get_transacao(id : int):
    mostrar_uma_transacao(id)
    
@router.post("transacao")
def post_transacao(transacao : Transacao, response : Response):
    criar_transacao(transacao, response)
    
@router.patch("transacao/{id}")
def patch_transacao(id: int, transacao_update : TransacaoUpdate, response : Response):
    atualizar_transacao(id , transacao_update , response)
    
@router.delete("transacao/{id}")
def delete_transacao(id : int):
    deletar_transacao(id)
    
@router.get("saldo")
def get_saldo():
    mostrar_saldo()