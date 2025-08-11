from fastapi import APIRouter, Query, Response, Depends
from auth.auth_service import get_current_user
from service.transacao_service import * 
from typing import Optional
router = APIRouter(prefix="/transacao", tags=["Transações"])

@router.get("", summary="Listar todas as transações")
async def get_transacoes(
    current_user_id : str = Depends(get_current_user),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo: entrada ou saida")
    ):
    return await lista_transacao(current_user_id, tipo)
    
@router.get("/{id}", summary="Obter uma transação específica" )
async def get_transacao(id : int, current_user_id : str = Depends(get_current_user)):
    return await mostrar_uma_transacao(id, current_user_id)
    
@router.post("", summary="Criar nova transação")
async def post_transacao(
    transacao : TransacaoCreate,
    response : Response,
    current_user_id : str = Depends(get_current_user)
                         ):
    return await criar_transacao(transacao, response, current_user_id)
    
@router.patch("/{id}", summary="Atualizar transação existente")
async def patch_transacao(
    id: int, 
    transacao_update : TransacaoUpdate,
    response : Response,
    current_user_id : str = Depends(get_current_user)
    ):
    return await atualizar_transacao(id , transacao_update , response, current_user_id)
    
@router.delete("/{id}", summary="Excluir transação")
async def delete_transacao(id : int, current_user_id : str = Depends(get_current_user)):
    return await deletar_transacao(id, current_user_id)
    