from fastapi import APIRouter, Query, Response, Depends
from auth.auth_service import get_current_user
from service.transacao_service import * 
from typing import Optional
router = APIRouter()

@router.get("transacao")
async def get_transacoes(
    current_user_id : str = Depends(get_current_user),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo: entrada ou saida")
    ):
    await lista_transacao(current_user_id, tipo)
    
@router.get("transacao/{id}")
async def get_transacao(id : int, current_user_id : str = Depends(get_current_user)):
    await mostrar_uma_transacao(id, current_user_id)
    
@router.post("transacao")
async def post_transacao(
    transacao : TransacaoCreate,
    response : Response,
    current_user_id : str = Depends(get_current_user)
                         ):
    await criar_transacao(transacao, response, current_user_id)
    
@router.patch("transacao/{id}")
async def patch_transacao(
    id: int, 
    transacao_update : TransacaoUpdate,
    response : Response,
    current_user_id : str = Depends(get_current_user)
    ):
    await atualizar_transacao(id , transacao_update , response, current_user_id)
    
@router.delete("transacao/{id}")
async def delete_transacao(id : int, current_user_id : str = Depends(get_current_user)):
    await deletar_transacao(id, current_user_id)
    
@router.get("saldo")
async def get_saldo(current_user_id : str = Depends(get_current_user)):
    await mostrar_saldo(current_user_id)