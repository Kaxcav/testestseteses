import sqlite3
import hashlib
import os
from datetime import datetime

DB_PATH = "pedidos.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS pedidos (
            id TEXT PRIMARY KEY, nome TEXT NOT NULL, email TEXT NOT NULL,
            telefone TEXT, cpf TEXT, quantidade INTEGER DEFAULT 1,
            total REAL NOT NULL, status TEXT DEFAULT 'aguardando_pagamento', criado_em TEXT NOT NULL)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL, senha_hash TEXT, google_id TEXT,
            avatar_url TEXT, criado_em TEXT NOT NULL)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS carrinho (
            id INTEGER PRIMARY KEY AUTOINCREMENT, usuario_id INTEGER NOT NULL,
            produto_id TEXT NOT NULL, nome TEXT NOT NULL, preco REAL NOT NULL,
            preco_antigo REAL NOT NULL, quantidade INTEGER DEFAULT 1,
            adicionado_em TEXT NOT NULL, FOREIGN KEY(usuario_id) REFERENCES usuarios(id))""")
        conn.commit()
    print("✅ Banco iniciado")

def hash_senha(senha):
    salt = os.environ.get("SALT","ml_salt_2025")
    return hashlib.sha256(f"{salt}{senha}".encode()).hexdigest()

def criar_usuario(nome, email, senha=None, google_id=None, avatar_url=None):
    senha_hash = hash_senha(senha) if senha else None
    try:
        with get_conn() as conn:
            conn.execute("""INSERT INTO usuarios (nome,email,senha_hash,google_id,avatar_url,criado_em)
                VALUES (?,?,?,?,?,?)""", (nome, email, senha_hash, google_id, avatar_url,
                datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            conn.commit()
        return buscar_usuario_por_email(email)
    except Exception as e:
        if "UNIQUE" in str(e): return None
        raise

def buscar_usuario_por_email(email):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM usuarios WHERE email=?", (email,)).fetchone()
    return dict(row) if row else None

def buscar_usuario_por_id(uid):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM usuarios WHERE id=?", (uid,)).fetchone()
    return dict(row) if row else None

def buscar_usuario_por_google(gid):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM usuarios WHERE google_id=?", (gid,)).fetchone()
    return dict(row) if row else None

def verificar_senha(email, senha):
    u = buscar_usuario_por_email(email)
    if u and u.get("senha_hash") == hash_senha(senha): return u
    return None

def atualizar_google_id(uid, google_id, avatar_url=None):
    with get_conn() as conn:
        conn.execute("UPDATE usuarios SET google_id=?,avatar_url=? WHERE id=?", (google_id, avatar_url, uid))
        conn.commit()

PRECO=54.95; PRECO_ANTIGO=71.44

def listar_carrinho(uid):
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM carrinho WHERE usuario_id=? ORDER BY adicionado_em DESC", (uid,)).fetchall()
    itens=[]
    for r in rows:
        i=dict(r)
        i["subtotal"]=round(PRECO_ANTIGO*i["quantidade"],2)
        i["desconto"]=round((PRECO_ANTIGO-PRECO)*i["quantidade"],2)
        i["total"]=round(PRECO*i["quantidade"],2)
        itens.append(i)
    return itens

def adicionar_ao_carrinho(uid, produto_id, nome, preco, preco_antigo, quantidade=1):
    with get_conn() as conn:
        ex = conn.execute("SELECT id,quantidade FROM carrinho WHERE usuario_id=? AND produto_id=?", (uid, produto_id)).fetchone()
        if ex:
            conn.execute("UPDATE carrinho SET quantidade=? WHERE id=?", (ex["quantidade"]+quantidade, ex["id"]))
        else:
            conn.execute("""INSERT INTO carrinho (usuario_id,produto_id,nome,preco,preco_antigo,quantidade,adicionado_em)
                VALUES (?,?,?,?,?,?,?)""", (uid, produto_id, nome, preco, preco_antigo, quantidade,
                datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        conn.commit()

def atualizar_quantidade_carrinho(uid, item_id, quantidade):
    with get_conn() as conn:
        if quantidade<=0: conn.execute("DELETE FROM carrinho WHERE id=? AND usuario_id=?", (item_id, uid))
        else: conn.execute("UPDATE carrinho SET quantidade=? WHERE id=? AND usuario_id=?", (quantidade, item_id, uid))
        conn.commit()

def remover_do_carrinho(uid, item_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM carrinho WHERE id=? AND usuario_id=?", (item_id, uid))
        conn.commit()

def limpar_carrinho(uid):
    with get_conn() as conn:
        conn.execute("DELETE FROM carrinho WHERE usuario_id=?", (uid,))
        conn.commit()

def total_itens_carrinho(uid):
    with get_conn() as conn:
        row = conn.execute("SELECT SUM(quantidade) as t FROM carrinho WHERE usuario_id=?", (uid,)).fetchone()
    return row["t"] or 0

def salvar_pedido(dados):
    with get_conn() as conn:
        conn.execute("""INSERT INTO pedidos (id,nome,email,telefone,cpf,quantidade,total,status,criado_em)
            VALUES (:id,:nome,:email,:telefone,:cpf,:quantidade,:total,:status,:criado_em)""",
            {**dados, "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
        conn.commit()

def listar_pedidos():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM pedidos ORDER BY criado_em DESC").fetchall()
    return [dict(r) for r in rows]

def atualizar_status_pedido(pedido_id, novo_status):
    with get_conn() as conn:
        conn.execute("UPDATE pedidos SET status=? WHERE id=?", (novo_status, pedido_id))
        conn.commit()
