from models.transacao_model import Transacao, TransacaoUpdate, TransacaoCreate
from typing import List, Optional
from core.database import *
from datetime import datetime
from view.transacao_view import *
from fastapi import HTTPException, Response, status

def lista_transacao(tipo: Optional[str] = None) -> List[Transacao]:
    try: 
        transacaoes = get_transacaoes(tipo)
        return exibir_transacoes(transacaoes)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar transação: {str(e)}")

        
def mostrar_uma_transacao(id : int) -> dict:
    try:    
        transacao = get_transacao_by_id(id)
        if not transacao:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar transação: {str(e)}")
def criar_transacao(transacao : TransacaoCreate, response : Response):
    try:
        nova_transacao = criar_transacao(transacao)
        response.status_code = status.HTTP_201_CREATED
        return criacao_sucedida(nova_transacao)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar transação: {str(e)}")

def atualizar_transacao(id: int, update_data : TransacaoUpdate, response : Response):
    try:
        transacao_atualizada = update_transacao(id, update_data)
        
        if not transacao_atualizada:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        response.status_code = status.HTTP_202_ACCEPTED
        return atualizacao_sucedida(id)
    except:    
        raise HTTPException(status_code= 404, detail="Transação não encontrada")

def deletar_transacao(id : int, response : Response) -> dict:
    try:
        if not delete_transacao(id):
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        response.status_code = status.HTTP_204_NO_CONTENT
        return delecao_sucedida(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar transação: {str(e)}")

    
    
def mostrar_saldo() -> dict:
    try:
        totais = get_saldo()
        
        if totais["receita"] == 0  and totais["despesa"] == 0:
            raise HTTPException(status_code=404, detail=f"Não há transações para calcular o saldo")
        
        return exibir_saldo_receita_despesa(
            despesa=totais["saida"],
            receita= totais["receita"],
            saldo= totais["saldo"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular saldo: {str(e)}")
    