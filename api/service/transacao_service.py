from models.transacao_model import Transacao, TransacaoUpdate
from typing import List, Optional
from database.fake_db import fake_db, entrada , saida
from datetime import datetime
from view.transacao_view import *
from fastapi import HTTPException, Response, status

def lista_transacao(tipo: Optional[str] = None) -> List[Transacao]:
    if tipo:
        tipo = tipo.lower()
        if tipo not in ["entrada", "saida"]:
            raise ValueError("Tipo deve ser 'entrada' ou 'saida'")
        return [t for t in fake_db if t.tipo == tipo]
    return exibir_transacoes()

def mostrar_uma_transacao(id : int):
    for transacao in fake_db:
        if Transacao.id == id:
            return exibir_transacao(transacao)
    ValueError("por favor, digite um id valido")
    
def criar_transacao(transacao : Transacao, response : Response):
    if any(transacao_existente.id == transacao.id for transacao_existente in fake_db):
        raise HTTPException(status_code=400, detail= "a tarefa ja existe no banco de dados")
    
    fake_db.append(transacao)
    response.status_code = status.HTTP_201_CREATED
    return criacao_sucedida(transacao.id, transacao.tipo)

def atualizar_transacao(id: int, dado : TransacaoUpdate, response : Response):
    for transacao in fake_db:
        if transacao.id == id:
            if dado.valor is not None:
                transacao.valor = dado.valor
            if dado.tipo is not None:
                transacao.tipo = dado.tipo.lower()
            if dado.descricao is not None:
                transacao.descricao = dado.descricao
            if dado.data is not None:
                transacao.data = datetime.now()
                
            response.status_code = status.HTTP_201_CREATED
            return atualizacao_sucedida(id)
        
    raise HTTPException(status_code= 404, detail="Transação não encontrada")

def deletar_transacao(id : int, response : Response):
    for transacao in fake_db:
        if transacao.id == id:
            fake_db.remove(transacao)
        response.status_code = status.HTTP_204_NO_CONTENT
        return delecao_sucedida
    raise HTTPException(status_code= 404 , detail="Transação não encontrada")
    
def mostrar_saldo():
    for trafego in fake_db:
        if trafego.tipo.lower() == "entrada":
            entrada.append(trafego.valor)
        elif trafego.tipo.lower() == "saida":
            saida.append(trafego.valor)
            
        if not entrada and not saida:
            raise HTTPException(status_code=404, detail="Não há transações para calcular o saldo")
        
        receita = sum(entrada)
        despesa = sum(saida)
        saldo_total = receita - despesa
        
        return exibir_saldo_receita_despesa(despesa= despesa, receita=receita, saldo=saldo_total)
    
    