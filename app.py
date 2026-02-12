from flask import Flask, request, jsonify
import os
from database import iniciar_banco, buscar_produto, adicionar_produto

app = Flask(__name__)

# Inicia o banco assim que o servidor liga
iniciar_banco()

@app.route('/')
def home():
    return "🟢 ATLAS SYSTEM V2: CÉREBRO ATIVO"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"📩 Payload recebido: {data}")
    
    # Simulação: Pegando dados como se viessem do WhatsApp
    # Na vida real, o JSON do WhatsApp é mais complexo, mas vamos simplificar para o teste
    msg = data.get('msg', '').lower()
    telefone = data.get('telefone', '')
    empresa_id = 1 # Por enquanto, vamos fingir que é tudo da Empresa 1 (Seu José)

    resposta = ""

    # --- LÓGICA DE ADMIN ---
    if msg.startswith("#admin add"):
        # Ex: #admin add cimento 500 10
        partes = msg.split()
        if len(partes) == 5:
            nome = partes[2]
            preco = float(partes[3])
            estoque = int(partes[4])
            if adicionar_produto(empresa_id, nome, preco, estoque):
                resposta = f"✅ Produto {nome} adicionado com sucesso!"
            else:
                resposta = "❌ Erro ao adicionar."
        else:
            resposta = "⚠️ Formato errado. Use: #admin add [nome] [preco] [qtd]"

    # --- LÓGICA DE CLIENTE ---
    else:
        # Tenta achar o produto
        produto = buscar_produto(empresa_id, msg)
        if produto:
            nome_prod, preco_prod, estoque_prod = produto
            resposta = f"🔎 Encontrei {nome_prod}!\n💰 Preço: {preco_prod} MT\n📦 Estoque: {estoque_prod}"
        else:
            resposta = "🤖 Olá! Digite o nome de um produto para ver o preço."

    return jsonify({"resposta_atlas": resposta})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
