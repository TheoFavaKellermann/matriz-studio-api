from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# Libera o acesso para a Loja e o Painel da Produção
CORS(app)

# Lista em memória para guardar os pedidos JSON
pedidos = []

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "sistema": "API Matriz Studio - PCP SENAI",
        "total_pedidos": len(pedidos)
    }), 200

# Rota para a Loja enviar novos pedidos (POST)
@app.route('/api/pedidos', methods=['POST'])
def criar_pedido():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Nenhum dado JSON enviado"}), 400
        
        pedidos.append(dados)
        print("Novo pedido recebido:", dados)
        
        return jsonify({
            "status": "sucesso",
            "mensagem": "Pedido registrado com sucesso!",
            "pedido": dados
        }), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota para o Painel da Produção consultar os pedidos (GET)
@app.route('/api/pedidos', methods=['GET'])
def listar_pedidos():
    return jsonify(pedidos), 200

# Rota para limpar os pedidos entre os testes na apresentação (DELETE)
@app.route('/api/pedidos/limpar', methods=['DELETE'])
def limpar_pedidos():
    global pedidos
    pedidos = []
    return jsonify({"status": "sucesso", "mensagem": "Lista de pedidos limpa!"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)