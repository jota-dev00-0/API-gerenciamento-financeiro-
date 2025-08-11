from models.transacao_model import Transacao
from typing import Optional, List
def exibir_transacao(transacao : Transacao):
    return {
        "message" : f"transacao no VALOR de {transacao.valor} do TIPO {transacao.tipo} ",
        "id" : transacao.id,
        "valor": transacao.valor,
        "tipo": transacao.tipo,
        "descricao": transacao.descricao,
        "data": transacao.data.isoformat() if transacao.data else None
    }
    
def exibir_transacoes(transacoes : List[Transacao]):
    return {
        "quantidade de transacoes" : len(transacoes),
        "transacoes" : [exibir_transacao(t) for t in transacoes]
    }
    
def criacao_sucedida(transacao : Transacao):
    return{
        "message" : "transacao criada com sucesso",
        "tipo" : transacao.tipo,
        "id" : transacao.id
    }
    
def atualizacao_sucedida(transacao : Transacao):
    return{
        "message": "Transação atualizada com sucesso", 
        "id": transacao.id
    }
    
def delecao_sucedida(transacao : Transacao):
    return{
        "message": "Transação deleta com sucesso", 
        "id": transacao.id
    }
    
