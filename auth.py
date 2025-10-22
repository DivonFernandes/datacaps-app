from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']

        with sqlite3.connect('usuarios.db') as conn:
            c = conn.cursor()
            c.execute("SELECT password FROM usuarios WHERE username=?", (usuario,))
            result = c.fetchone()
            if result and senha == result[0]:
                session['logado'] = True
                return redirect(url_for('views.ssma'))
        return "Login inválido!"
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('auth.login'))