from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados SQLite
def connect_db():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row  # Permite acesso aos resultados como dicionários
    return conn

# ------- TICKETS --------

# Pegar todos os tickets
@app.route('/tickets', methods=['GET'])
def get_all_tickets():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Ticket")
    tickets = cursor.fetchall()
    conn.close()
    tickets = [dict(ticket) for ticket in tickets]
    return jsonify(tickets)

# Cadastrar um ticket (Status sempre 0, ID_pessoa sempre NULL)
@app.route('/tickets', methods=['POST'])
def create_ticket():
    dados = request.get_json()
    Titulo = dados.get('Titulo')
    if not Titulo:
        return jsonify({"error": "O campo 'Titulo' é obrigatório."}), 400

    Descricao = dados.get('Descricao')
    Prioridade = dados.get('Prioridade')

    # Status sempre 0 (Aberto)
    Status = 0

    # ID_pessoa sempre NULL
    ID_pessoa = None

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Ticket (Titulo, Descricao, Prioridade, Status, ID_pessoa) 
        VALUES (?, ?, ?, ?, ?)
    """, (Titulo, Descricao, Prioridade, Status, ID_pessoa))
    conn.commit()
    conn.close()
    return jsonify({"status": "Ticket criado com sucesso!"}), 201

# Atualizar um ticket (somente Prioridade, Status e ID_pessoa)
@app.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    dados = request.get_json()
    Prioridade = dados.get('Prioridade')
    Status = dados.get('Status')
    ID_pessoa = dados.get('ID_pessoa')

    if Prioridade is None and Status is None and ID_pessoa is None:
        return jsonify({"error": "É necessário fornecer ao menos um dos campos: 'Prioridade', 'Status' ou 'ID_pessoa'."}), 400

    # Validação do Status
    if Status is not None and Status not in [0, 1, 2]:
        return jsonify({"error": "O campo 'Status' deve ser 0 (Aberto), 1 (Em Andamento) ou 2 (Completo)."}), 400

    conn = connect_db()
    cursor = conn.cursor()

    # Construir a query dinamicamente com base nos campos fornecidos
    campos = []
    valores = []

    if Prioridade is not None:
        campos.append('Prioridade = ?')
        valores.append(Prioridade)
    if Status is not None:
        campos.append('Status = ?')
        valores.append(Status)
    if ID_pessoa is not None:
        campos.append('ID_pessoa = ?')
        valores.append(ID_pessoa)

    valores.append(ticket_id)
    query = f"UPDATE Ticket SET {', '.join(campos)} WHERE ID = ?"

    cursor.execute(query, valores)
    conn.commit()
    conn.close()
    return jsonify({"status": "Ticket atualizado com sucesso!"})

# Puxar tickets abertos (Status = 0)
@app.route('/tickets/abertos', methods=['GET'])
def get_open_tickets():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Ticket WHERE Status = 0")
    tickets = cursor.fetchall()
    conn.close()
    tickets = [dict(ticket) for ticket in tickets]
    return jsonify(tickets)

# Puxar tickets em andamento (Status = 1)
@app.route('/tickets/andamento', methods=['GET'])
def get_in_progress_tickets():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Ticket WHERE Status = 1")
    tickets = cursor.fetchall()
    conn.close()
    tickets = [dict(ticket) for ticket in tickets]
    return jsonify(tickets)

# Puxar tickets completos (Status = 2)
@app.route('/tickets/completos', methods=['GET'])
def get_completed_tickets():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Ticket WHERE Status = 2")
    tickets = cursor.fetchall()
    conn.close()
    tickets = [dict(ticket) for ticket in tickets]
    return jsonify(tickets)

# Puxar tickets cadastrados por um usuário específico
@app.route('/tickets/usuario/<int:usuario_id>', methods=['GET'])
def get_tickets_by_user(usuario_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Ticket WHERE ID_pessoa = ?", (usuario_id,))
    tickets = cursor.fetchall()
    conn.close()
    tickets = [dict(ticket) for ticket in tickets]
    return jsonify(tickets)

# ------- USUÁRIOS --------

# Pegar todos os usuários
@app.route('/usuarios', methods=['GET'])
def get_all_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pessoas")
    users = cursor.fetchall()
    conn.close()
    users = [dict(user) for user in users]
    # Converter ADM de inteiro para booleano
    for user in users:
        user['ADM'] = bool(user['ADM'])
    return jsonify(users)

# Pegar usuário com base no ID
@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
def get_user_by_id(usuario_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pessoas WHERE ID = ?", (usuario_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        user = dict(user)
        user['ADM'] = bool(user['ADM'])
        return jsonify(user)
    return jsonify({"error": "Usuário não encontrado"}), 404

# Pegar usuário com base no Login
@app.route('/usuarios/login/<string:login>', methods=['GET'])
def get_user_by_login(login):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pessoas WHERE Login = ?", (login,))
    user = cursor.fetchone()
    conn.close()
    if user:
        user = dict(user)
        user['ADM'] = bool(user['ADM'])
        return jsonify(user)
    return jsonify({"error": "Usuário não encontrado"}), 404

# Cadastrar usuário (ADM sempre 0)
@app.route('/usuarios', methods=['POST'])
def create_user():
    dados = request.get_json()
    Login = dados.get('Login')
    Senha = dados.get('Senha')

    if not all([Login, Senha]):
        return jsonify({"error": "Os campos 'Login' e 'Senha' são obrigatórios."}), 400

    # ADM sempre 0
    ADM_int = 0

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Pessoas (Login, Senha, ADM) VALUES (?, ?, ?)", 
                       (Login, Senha, ADM_int))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "O 'Login' fornecido já está em uso."}), 400
    finally:
        conn.close()
    return jsonify({"status": "Usuário criado com sucesso!"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
