from flask import Flask, render_template, request, redirect, session, url_for
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)

# 🔐 segredo da sessão
app.secret_key = os.getenv("SECRET_KEY")

# 👤 credenciais
ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS = os.getenv("ADMIN_PASS")

# ⏱ tempo de sessão
SESSION_TIMEOUT = 10  # segundos

# 📄 logs
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# -------------------
# 🏠 TELA PÚBLICA
# -------------------
@app.route('/')
def index():
    return render_template('index.html')


# -------------------
# 🔐 LOGIN
# -------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')

        # 🔒 validação simples
        if not user or not password:
            return "Campos obrigatórios!"

        if user == ADMIN_USER and password == ADMIN_PASS:
            session['user'] = user
            session['last_activity'] = datetime.now().isoformat()
            logging.info("Login bem-sucedido")
            return redirect('/admin')
        else:
            logging.warning("Tentativa de login inválida")
            return "Login inválido"

    return render_template('login.html')


# -------------------
# 🔐 ÁREA ADMIN
# -------------------
@app.route('/admin')
def admin():
    if 'user' not in session:
        logging.warning("Acesso negado à área admin")
        return redirect('/login')

    # ⏱ controle de tempo
    last_activity = datetime.fromisoformat(session['last_activity'])
    if datetime.now() - last_activity > timedelta(seconds=SESSION_TIMEOUT):
        session.clear()
        logging.info("Sessão expirada")
        return redirect('/')

    session['last_activity'] = datetime.now().isoformat()

    return render_template('admin.html')


# -------------------
# 💡 AÇÃO ADMIN (EX: LED)
# -------------------
@app.route('/ligar_led')
def ligar_led():
    if 'user' not in session:
        logging.warning("Tentativa de acesso sem login (LED)")
        return redirect('/login')

    logging.info("LED acionado pelo admin")

    # aqui você colocaria o GPIO
    return "LED LIGADO"


# -------------------
# 🚪 LOGOUT
# -------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# -------------------
# 🚀 EXECUÇÃO SEGURA
# -------------------
if __name__ == '__main__':
    app.run(debug=False)