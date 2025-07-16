from models.transacao_model import Transacao
from database.fake_db import fake_db
from typing import Optional
def exibir_transacao(transacao : Transacao):
    return {
        "message" : f"transacao no VALOR de {transacao.valor} do TIPO {transacao.tipo} ",
        "id" : transacao.id
    }
    
def exibir_transacoes():
    return {
        "quantidade de transacoes" : len(fake_db),
        "transacoes" : fake_db
    }
    
def criacao_sucedida(id : int, tipo : Optional[str] = None):
    return{
        "message" : "transacao criada com sucesso",
        "tipo" : tipo,
        "id" : id
    }
    
def atualizacao_sucedida(id : int):
    return{
        "message": "Transação atualizada com sucesso", 
        "id": id
    }
    
def delecao_sucedida(id : id):
    return{
        "message": "Transação deleta com sucesso", 
        "id": id
    }
    
def exibir_saldo_receita_despesa(despesa : float, receita : float, saldo : float):
    return{
        "saldo" : saldo,
        "receita" : receita,
        "despesa" : despesa 
    }