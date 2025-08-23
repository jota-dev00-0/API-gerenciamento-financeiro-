import os
import sqlite3 
from typing import Optional, List, Dict
from dotenv import load_dotenv
from models.transacao_model import TransacaoUpdate, TransacaoCreate, Transacao
from models.user_model import UserDB, UserCreate
from datetime import datetime
from utils.security import criar_hash_senha 


load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "financas.sqlite")
SQL_SCRIPT_PATH = os.path.join(BASE_DIR, "database", "financas.sql")


os.makedirs(DB_DIR, exist_ok=True)


with open(SQL_SCRIPT_PATH, "r", encoding="utf-8") as f:
    sql_script = f.read()  


conn = sqlite3.connect(DB_PATH)
conn.executescript(sql_script)
conn.commit()
conn.close()

print(f"Banco de dados criado com sucesso em: {DB_PATH}")
    
    
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_database_connection():
    print(f"DB_DIR existe: {os.path.exists(DB_DIR)}")
    print(f"DB_DIR tem permissão de escrita: {os.access(DB_DIR, os.W_OK)}")
    print(f"SQL_SCRIPT_PATH existe: {os.path.exists(SQL_SCRIPT_PATH)}")
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar com o banco: {e}")
        print(f"Caminho tentado: {DB_PATH}")
        raise
    

def get_transacaoes (user_id: str, tipo : Optional[str] = None) -> List[Transacao]:
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        if tipo:
            cursor.execute("SELECT * FROM transacao WHERE user_id = ? AND tipo", (user_id , tipo, ))
        else:
            cursor.execute("SELECT * FROM transacao WHERE user_id = ? " , (user_id,))
        return [Transacao(**dict(row))  for row in cursor.fetchall() ]
    finally:
        conn.close()
    


def get_transacao_by_id (transacao_id : int, user_id : str) -> Optional[Transacao]:
    conn =  get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM transacao WHERE id = ? AND user_id = ?", (transacao_id, user_id,))
        row = cursor.fetchone()
        return Transacao(**dict(row)) if row else None
    finally:
        conn.close()

        
def create_transacao(transacao_data : dict) -> Transacao:
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            " INSERT INTO transacao (valor, tipo, descricao, user_id, data) VALUES (? , ? , ?, ?, ?)",
            (
                transacao_data["valor"], 
                transacao_data["tipo"],
                transacao_data.get("descricao"),
                transacao_data["user_id"],
                transacao_data["data"].strftime("%Y-%m-%d %H:%M:%S")
        
            )
        )
        conn.commit()
        trasansacao_id = cursor.lastrowid
        cursor.execute("SELECT * FROM transacao WHERE id = ?" , (trasansacao_id))
        new_transacao = cursor.fetchone()
        if new_transacao:
            return Transacao(**dict(new_transacao))
    finally:
        conn.close()

        
def update_transacao (transacao_id : int , update_data : TransacaoUpdate, user_id : str) -> Optional[Transacao]:
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        set_clause = []
        values = []
        for key, value in update_data.model_dump(exclude_unset=True).items():
            if value is not None:
                set_clause.append(f"{key} = ?")
                values.append(value)
                
        if not set_clause:
            return None
        
        values.append([transacao_id, user_id])
        query = f"UPDATE transacao SET {','.join(set_clause)} WHERE id = ? AND user_id = ?"
        cursor.execute(query, tuple(values))
        conn.commit()
        
        cursor.execute("SELECT * FROM transacao WHERE id = ? AND user_id = ?", (transacao_id, user_id,))
        row = cursor.fetchone()
        return Transacao(**dict(row)) if update_transacao else None
    finally:
        conn.close()
    
    
    


def delete_transacao_db (transacao_id : id, user_id : str) -> bool:
    conn = get_database_connection()
    cursor = conn.cursor()
    try: 
        cursor.execute("DELETE FROM transacao WHERE id = ? AND id = ?" ,
                       (transacao_id, user_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
    


def get_saldo (user_id : str) -> Dict[str, float]:
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT tipo , SUM(valor) as total from transacao WHERE user_id = ? GROUP BY tipo"
            , (user_id,)
            )
        rows = cursor.fetchall()
        
        totais = {"entrada" : 0.0, "saida" : 0.0}
        for row in rows:
            tipo = row['tipo']
            total = row['total'] or 0.0
            totais[tipo] = total
            
        receitas = totais["entrada"]
        despesas = totais["saida"]
        saldo_final = receitas - despesas 
        return {
            "receitas" : receitas ,
            "despesas" : despesas,
            "saldo" : saldo_final
            }
    finally:
        conn.close()
        
def create_user_db( user_data : dict) -> UserDB:
    conn = get_database_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO user (nome, email, senha) VALUES (?, ? , ?)",
                       (
                        user_data["nome"],
                        user_data["email"],
                        user_data["senha_hash"]
                       ))
        conn.commit()
        last_user_id = cursor.lastrowid
        cursor.execute("SELECT * FROM user WHERE id = ? ", (last_user_id,))
        user_created = cursor.fetchone()
        
        if user_created:
            return UserDB(
                id=user_created["id"],
                nome=user_created["nome"],
                email=user_created["email"],
                senha_hash=user_created["senha"],
            )
        
        
        return None
    finally:
        conn.close()
    
        
def get_user_by_email_db(email : str) -> Optional[UserDB]:
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, nome, email, senha FROM user WHERE email = ?", 
            (email,)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return UserDB(
                id=user['id'],
                nome=user['nome'],
                email=user['email'],
                senha_hash=user['senha']
            )
        return None  # ← Retorne None, não uma string
    except Exception as e:
        conn.close()
        print(f"Erro ao buscar usuário por email: {e}")
        return None