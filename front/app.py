# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Middleware API base URL
#API_URL = 'http://localhost:8000'  # Adjust if necessary

# bom dia antonio

# Middleware API base URL
API_URL = 'http://192.168.100.11:8000'

# app.py

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_data = {
            'Login': request.form['login'],
            'Senha': request.form['senha']
        }
        print("\n[LOGIN] Sending POST request to middleware:")
        print(f"URL: {API_URL}/login")
        print(f"Data: {login_data}")
        response = requests.post(f"{API_URL}/login", json=login_data)
        print("[LOGIN] Received response from middleware:")
        print(f"Status code: {response.status_code}")
        print(f"Response content: {response.text}\n")
        if response.status_code == 200:
            user = response.json()
            session['user_id'] = user['ID']
            session['login'] = user['Login']
            session['adm'] = user['ADM']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid login credentials.', 'danger')
    return render_template('login.html')

# app.py

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        register_data = {
            'Login': request.form['login'],
            'Senha': request.form['senha'],
            'ADM': False  # Default to regular user
        }
        print("\n[REGISTER] Sending POST request to middleware:")
        print(f"URL: {API_URL}/register")
        print(f"Data: {register_data}")
        response = requests.post(f"{API_URL}/register", json=register_data)
        print("[REGISTER] Received response from middleware:")
        print(f"Status code: {response.status_code}")
        print(f"Response content: {response.text}\n")
        if response.status_code == 201:
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            error_message = response.json().get('detail', 'Error creating account.')
            flash(error_message, 'danger')
    return render_template('register.html')

# app.py

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    if session['adm']:
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('user_dashboard'))

# app.py

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'user_id' not in session or not session['adm']:
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        ticket_data = {
            'Titulo': request.form['titulo'],
            'Descricao': request.form['descricao'],
            'Prioridade': int(request.form['prioridade'])
        }
        print("\n[ADMIN DASHBOARD] Sending POST request to middleware to create a ticket:")
        print(f"URL: {API_URL}/tickets")
        print(f"Data: {ticket_data}")
        response = requests.post(f"{API_URL}/tickets", json=ticket_data)
        print("[ADMIN DASHBOARD] Received response from middleware:")
        print(f"Status code: {response.status_code}")
        print(f"Response content: {response.text}\n")
        if response.status_code == 201:
            flash('Ticket created successfully!', 'success')
        else:
            error_message = response.json().get('detail', 'Error creating ticket.')
            flash(error_message, 'danger')
    return render_template('admin_dashboard.html')

# app.py

@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session or session['adm']:
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))
    # Get open tickets
    print("\n[USER DASHBOARD] Sending GET request to middleware to get open tickets:")
    print(f"URL: {API_URL}/tickets/open")
    response = requests.get(f"{API_URL}/tickets/open")
    print("[USER DASHBOARD] Received response from middleware:")
    print(f"Status code: {response.status_code}")
    print(f"Response content: {response.text}\n")
    if response.status_code == 200:
        tickets = response.json()
    else:
        tickets = []
        flash('Error fetching tickets.', 'danger')
    return render_template('user_dashboard.html', tickets=tickets)

# app.py

@app.route('/assign_ticket/<int:ticket_id>', methods=['POST'])
def assign_ticket(ticket_id):
    if 'user_id' not in session or session['adm']:
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    print("\n[ASSIGN TICKET] Sending PUT request to middleware to assign ticket:")
    print(f"URL: {API_URL}/tickets/{ticket_id}/assign/{user_id}")
    
    # Fazendo a requisição PUT para a nova rota do middleware
    response = requests.put(f"{API_URL}/tickets/{ticket_id}/assign/{user_id}")
    print("[ASSIGN TICKET] Received response from middleware:")
    print(f"Status code: {response.status_code}")
    print(f"Response content: {response.text}\n")
    
    if response.status_code == 200:
        flash('Ticket assigned to you!', 'success')
    else:
        error_message = response.json().get('detail', 'Error assigning ticket.')
        flash(error_message, 'danger')
    
    return redirect(url_for('user_dashboard'))



# app.py

@app.route('/my_tickets')
def view_assigned_tickets():
    if 'user_id' not in session or session['adm']:
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))
    user_id = session['user_id']
    print("\n[MY TICKETS] Sending GET request to middleware to get tickets assigned to user:")
    print(f"URL: {API_URL}/tickets/user/{user_id}")
    response = requests.get(f"{API_URL}/tickets/user/{user_id}")
    print("[MY TICKETS] Received response from middleware:")
    print(f"Status code: {response.status_code}")
    print(f"Response content: {response.text}\n")
    if response.status_code == 200:
        tickets = response.json()
    else:
        tickets = []
        flash('Error fetching your tickets.', 'danger')
    return render_template('assigned_tickets.html', tickets=tickets)

# app.py

@app.route('/complete_ticket/<int:ticket_id>', methods=['POST'])
def complete_ticket(ticket_id):
    if 'user_id' not in session or session['adm']:
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    # Construir os dados para a requisição PUT conforme necessário pelo middleware
    data = {
        'ID_pessoa': session['user_id'],  # Usuário que está completando o ticket
        'Status': 2  # Status indicando que o ticket foi resolvido
    }

    print("\n[COMPLETE TICKET] Sending PUT request to middleware to complete ticket:")
    print(f"URL: {API_URL}/tickets/complete/{ticket_id}")
    print(f"Data: {data}")
    
    response = requests.put(f"{API_URL}/tickets/complete/{ticket_id}", json=data)
    print("[COMPLETE TICKET] Received response from middleware:")
    print(f"Status code: {response.status_code}")
    print(f"Response content: {response.text}\n")
    
    if response.status_code == 200:
        flash('Ticket completed!', 'success')
    else:
        try:
            error_message = response.json().get('detail', 'Error completing ticket.')
        except ValueError:
            error_message = 'Error completing ticket.'
        flash(error_message, 'danger')

    return redirect(url_for('view_assigned_tickets'))

# app.py

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))
