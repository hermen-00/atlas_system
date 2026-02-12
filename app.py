
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
# Pega a porta do ambiente ou usa 5000 se estiver no Termux local
PORT = int(os.environ.get("PORT", 1000))

@app.route('/')
def home():
    """Rota de teste para ver se o servidor está vivo."""
    return "🟢 ATLAS SYSTEM V1.0: ONLINE (MOZAMBIQUE NODE)"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Aqui é onde o WhatsApp vai bater na porta."""
    data = request.json
    print(f"📩 Recebido: {data}")
    
    # Por enquanto, só confirma o recebimento
    return jsonify({"status": "recebido", "mensagem": "Atlas escutando..."}), 200

if __name__ == '__main__':
    # Debug=True ajuda a ver erros no Termux, mas desligaremos em produção
    app.run(host='0.0.0.0', port=PORT, debug=True)
