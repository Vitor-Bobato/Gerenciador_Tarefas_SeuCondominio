from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Lista de tarefas para simular um banco de dados
# Adicionamos a propriedade 'descricao' e mais opções de 'status'
tarefas = [
    {
        'id': 1,
        'nome': 'Manutenção do portão',
        'custo': 150.00,
        'data_inicio': '2025-08-01',
        'data_conclusao': '2025-08-05',
        'status': 'Concluída',
        'descricao': 'Conserto do motor do portão principal e lubrificação das dobradiças.',
        'comentarios': ['Orçamento aprovado.', 'Serviço finalizado com sucesso.']
    },
    {
        'id': 2,
        'nome': 'Limpeza da piscina',
        'custo': 80.50,
        'data_inicio': '2025-08-10',
        'data_conclusao': '2025-08-12',
        'status': 'Em Andamento',
        'descricao': 'Limpeza completa e tratamento químico da água.',
        'comentarios': ['Contratado o zelador.', 'Agendado para amanhã.']
    },
    {
        'id': 3,
        'nome': 'Vistoria de segurança',
        'custo': 0.00,
        'data_inicio': '2025-08-15',
        'data_conclusao': '2025-08-15',
        'status': 'Pendente',
        'descricao': 'Inspeção anual dos sistemas de alarme e câmeras.',
        'comentarios': []
    }
]

# Variável para gerar IDs de tarefas automaticamente
proximo_id = 4

# Rota principal para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# --- Rotas da API RESTful para Tarefas ---

# API para buscar todas as tarefas
@app.route('/api/tarefas', methods=['GET'])
def get_tarefas():
    return jsonify(tarefas)

# API para criar uma nova tarefa
@app.route('/api/tarefas', methods=['POST'])
def criar_tarefa():
    global proximo_id
    dados = request.get_json()
    nova_tarefa = {
        'id': proximo_id,
        'nome': dados.get('nome'),
        'custo': dados.get('custo'),
        'data_inicio': dados.get('data_inicio'),
        'data_conclusao': dados.get('data_conclusao'),
        'status': dados.get('status'),
        'descricao': dados.get('descricao', ''),  # Adiciona a nova propriedade de descrição
        'comentarios': []
    }
    tarefas.append(nova_tarefa)
    proximo_id += 1
    return jsonify(nova_tarefa), 201

# API para buscar uma única tarefa
@app.route('/api/tarefas/<int:tarefa_id>', methods=['GET'])
def get_tarefa(tarefa_id):
    tarefa_encontrada = next((tarefa for tarefa in tarefas if tarefa['id'] == tarefa_id), None)
    if tarefa_encontrada:
        return jsonify(tarefa_encontrada)
    return jsonify({'erro': 'Tarefa não encontrada'}), 404

# API para editar uma tarefa existente
@app.route('/api/tarefas/<int:tarefa_id>', methods=['PUT'])
def editar_tarefa(tarefa_id):
    dados = request.get_json()
    tarefa_encontrada = next((tarefa for tarefa in tarefas if tarefa['id'] == tarefa_id), None)

    if tarefa_encontrada:
        # Atualiza apenas os campos que foram enviados na requisição
        tarefa_encontrada.update(dados)
        return jsonify(tarefa_encontrada)
    return jsonify({'erro': 'Tarefa não encontrada'}), 404

# API para excluir uma tarefa
@app.route('/api/tarefas/<int:tarefa_id>', methods=['DELETE'])
def excluir_tarefa(tarefa_id):
    global tarefas
    tarefas = [t for t in tarefas if t['id'] != tarefa_id]
    return jsonify({'mensagem': 'Tarefa excluída com sucesso'}), 200

# --- Rotas da API para Comentários ---

# API para adicionar um comentário a uma tarefa
@app.route('/api/tarefas/<int:tarefa_id>/comentarios', methods=['POST'])
def adicionar_comentario(tarefa_id):
    dados = request.get_json()
    comentario = dados.get('comentario')
    
    tarefa_encontrada = next((tarefa for tarefa in tarefas if tarefa['id'] == tarefa_id), None)

    if tarefa_encontrada and comentario:
        tarefa_encontrada['comentarios'].append(comentario)
        return jsonify({'mensagem': 'Comentário adicionado com sucesso'}), 201
    
    return jsonify({'erro': 'Tarefa não encontrada ou comentário inválido'}), 400

if __name__ == '__main__':
    app.run(debug=True)