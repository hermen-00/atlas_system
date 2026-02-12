import sqlite3
import os

# Nome do banco de dados
DB_NAME = "atlas_memoria.db"

def conectar():
    """Conecta ao banco de dados."""
    return sqlite3.connect(DB_NAME)

def iniciar_banco():
    """Cria as tabelas se não existirem."""
    conn = conectar()
    cursor = conn.cursor()
    
    # Tabela 1: Empresas (Seu José, Seu Pedro...)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_dono TEXT,
            telefone_dono TEXT UNIQUE,
            saldo REAL DEFAULT 0.0
        )
    ''')

    # Tabela 2: Produtos (Com vínculo de empresa_id)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER,
            nome TEXT,
            preco REAL,
            estoque INTEGER,
            FOREIGN KEY(empresa_id) REFERENCES empresas(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ [ATLAS] Banco de dados inicializado!")

def buscar_produto(empresa_id, termo_busca):
    """Procura um produto específico daquela empresa."""
    conn = conectar()
    cursor = conn.cursor()
    termo = f"%{termo_busca}%"
    
    cursor.execute('''
        SELECT nome, preco, estoque FROM produtos 
        WHERE empresa_id = ? AND nome LIKE ?
    ''', (empresa_id, termo))
    
    resultado = cursor.fetchone()
    conn.close()
    return resultado

# Função para cadastrar produto (Usada no Modo Admin)
def adicionar_produto(empresa_id, nome, preco, estoque):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO produtos (empresa_id, nome, preco, estoque) VALUES (?, ?, ?, ?)",
                       (empresa_id, nome.lower(), preco, estoque))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False
    finally:
        conn.close()
