from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decimal import Decimal

db = SQLAlchemy()

# Tabela 1: Quem Manda (O Dono)
class Empresa(db.Model):
    __tablename__ = 'empresas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), unique=True, nullable=False)
    saldo_conta = db.Column(db.Numeric(10, 2), default=0.00) # Numeric para dinheiro!
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

# Tabela 2: O Produto (Com regras de comissão do PDF)
class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    estoque = db.Column(db.Integer, default=0)
    
    # Regras de Comissão [cite: 296, 340]
    comissao_pct = db.Column(db.Numeric(5, 2), default=5.00) # Ex: 5.00%
    min_fee = db.Column(db.Numeric(10, 2), default=0.50)     # Mínimo 0.50 MT
    
    # Controle de Concorrência (Versionamento) 
    versao = db.Column(db.Integer, default=1)

# Tabela 3: O Pedido Seguro
class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'))
    cliente_telefone = db.Column(db.String(20))
    
    # Status do PDF [cite: 206]
    status = db.Column(db.String(20), default='PENDENTE') # PENDENTE, RESERVADO, PAGO, CANCELADO
    valor_total = db.Column(db.Numeric(10, 2), default=0.00)
    comissao_total = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Chave de Idempotência (Anti-Duplicação) [cite: 373, 406]
    idempotency_key = db.Column(db.String(100), unique=True, nullable=True)
    
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

# Tabela 4: Itens do Pedido (Detalhe para cálculo linha a linha)
class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'))
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'))
    
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario_congelado = db.Column(db.Numeric(10, 2)) # Preço na hora da compra [cite: 429]
    comissao_calculada = db.Column(db.Numeric(10, 2))       # Comissão final desta linha [cite: 347]
