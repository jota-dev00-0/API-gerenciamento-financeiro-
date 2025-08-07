from models.transacao_model import Transacao, TransacaoUpdate, TransacaoCreate
from typing import List, Optional
from core.database import *
from datetime import datetime
from view.transacao_view import *
from fastapi import HTTPException, Response, status

def lista_transacao(user_id : str , tipo: Optional[str] = None) -> List[Transacao]:
    try: 
        transacaoes = get_transacaoes(user_id, tipo)
        return exibir_transacoes(transacaoes)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar transação: {str(e)}")

        
def mostrar_uma_transacao(id : int, user_id : str) -> Transacao:
    try:    
        transacao = get_transacao_by_id(id, user_id)
        if not transacao:
            raise HTTPException(status_code=404, detail="Transação não encontrada")  
        return transacao   
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar transação: {str(e)}")
    
def criar_transacao(transacao : TransacaoCreate, response : Response, user_id : str):
    try:
        transacao_data = {
            **transacao.model_dump(),
            "user_id" : user_id,
            "data" : datetime.now()
        }
        nova_transacao = create_transacao(transacao_data)
        if not nova_transacao:
            raise HTTPException(
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Falha ao criar transação"
                )
        response.status_code = status.HTTP_201_CREATED
        return criacao_sucedida(nova_transacao)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar transação: {str(e)}")

def atualizar_transacao(id: int, update_data : TransacaoUpdate, response : Response, user_id : str):
    try:
        transacao_atualizada = update_transacao(id, update_data, user_id)
        
        if not transacao_atualizada:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        response.status_code = status.HTTP_202_ACCEPTED
        return atualizacao_sucedida(id)
    except:    
        raise HTTPException(status_code= 404, detail="Transação não encontrada")
    

def deletar_transacao(id : int, response : Response, user_id : str) -> dict:
    try:
        if not delete_transacao_db(id, user_id):
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        response.status_code = status.HTTP_204_NO_CONTENT
        return delecao_sucedida(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar transação: {str(e)}")

    
    
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
    