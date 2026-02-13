import os
from flask import Flask, jsonify, request
from models import db, Empresa, Produto
from decimal import Decimal

app = Flask(__name__)

# CONFIGURAÇÃO DO BANCO DE DADOS
# Se tiver no Render, usa Postgres. Se tiver no Termux, usa arquivo local.
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///atlas_local.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco com o app
db.init_app(app)

# Cria as tabelas na primeira vez que rodar
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "🛡️ ATLAS ENTERPRISE: ONLINE (DB CONNECTED)"

# Rota de teste para ver se o banco grava de verdade
@app.route('/test-db', methods=['GET'])
def teste_db():
    try:
        # Tenta criar uma empresa de teste
        nova_empresa = Empresa(nome="Loja Teste", telefone="841234567")
        db.session.add(nova_empresa)
        db.session.commit()
        return jsonify({"status": "sucesso", "id": nova_empresa.id})
    except Exception as e:
        return jsonify({"status": "erro", "detalhe": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
