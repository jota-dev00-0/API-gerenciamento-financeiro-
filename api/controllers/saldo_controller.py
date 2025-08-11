from fastapi import APIRouter, Depends
from auth.auth_service import get_current_user
from service.saldo_service import mostrar_saldo

router = APIRouter(prefix="/saldo", tags=["Saldo"])

@router.get("", summary=" Exibir Saldo")
async def get_saldo(current_user_id : str = Depends(get_current_user)):
    await mostrar_saldo(current_user_id)
    
    