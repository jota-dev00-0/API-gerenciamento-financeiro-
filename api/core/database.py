import os
import sqlite3 
from typing import Optional, List
from dotenv import load_dotenv
from models.transacao_model import TransacaoUpdate, TransacaoCreate, Transacao



def get_database_connection():
    load_dotenv()
    DATABASE_PATH = os.getenv("DATABASE")
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_transacao(transacao : TransacaoCreate) -> Transacao:
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute(
        " INSERT INTO transacao (valor, tipo, descricao) VALUES (? , ? , ?)",
        (transacao.valor, transacao.tipo, transacao.descricao)
    )
    conn.commit()
    cursor.execute("SELECT * FROM transacao WHERE id = ?" , (cursor.lastrowid))
    new_transacao = cursor.fetchone()
    conn.close()
    return Transacao(**dict(new_transacao))

def get_transacaoes (tipo : Optional[str] = None) -> List[Transacao]:
    conn = get_database_connection()
    cursor = conn.cursor()
    
    if tipo:
        cursor.execute("SELECT * FROM transacao WHERE tipo = ?", (tipo,))
    else:
        cursor.execute("SELECT * FROM transacao ")
    transacoes = [Transacao(**dict(row))  for row in cursor.fetchall() ]
    conn.close()
    return transacoes


def get_transacao_by_id (transacao_id : int) -> Optional[Transacao]:
    conn =  get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacao WHERE id = ?", (transacao_id))
    transacao = cursor.fetchone()
    conn.close()
    
    return transacao

def update_transacao (transacao_id : int , update_data : TransacaoUpdate) -> Optional[Transacao]:
    conn = get_database_connection()
    cursor = conn.cursor()
    
    set_clause = []
    values = []
    for key, value in update_data.model_dump(exclude_unset=True).items():
        if value is not None:
            set_clause.append(f"{key} = ?")
            values.append(value)
            
    if not set_clause:
        return None
    
    values.append(transacao_id)
    query = f"UPDATE transacao SET {",".join(set_clause)} WHERE id = ?"
    cursor.execute(query, tuple(values))
    conn.commit()
    
    cursor.execute("SELECT * FROM transacao WHERE id = ?", (transacao_id))
    update_transacao = cursor.fetchone()
    conn.close()
    
    return Transacao(**dict(update_transacao)) if update_transacao else None


def delete_transacao (transacao_id : id) -> Optional[Transacao]:
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transacao WHERE id = ?" , (transacao_id))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def get_saldo ():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT tipo , SUM(valor) as total from transacao GROUP BY tipo")
    rows = cursor.fetchall()
    conn.close()
    
    totais = {"entrada" : 0.0, "saida" : 0.0}
    for row in rows:
        tipo = row['tipo']
        total = row['total'] or 0.0
        totais[tipo] = total
        
    receitas = totais["entrada"]
    despesas = totais["saida"]
    saldo_final = receitas - despesas 
    return {"receitas" : receitas , "despesas" : despesas, "saldo" : saldo_final}
    