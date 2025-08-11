from fastapi import HTTPException
from core.database import get_saldo
from view.saldo_view import exibir_saldo_receita_despesa
def mostrar_saldo(user_id : str) -> dict:
    try:
        totais = get_saldo(user_id)
        
        if totais["receita"] == 0  and totais["despesa"] == 0:
            raise HTTPException(status_code=404, detail=f"Não há transações para calcular o saldo")
        
        return exibir_saldo_receita_despesa(
            despesa=totais["saida"],
            receita= totais["receita"],
            saldo= totais["saldo"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular saldo: {str(e)}")