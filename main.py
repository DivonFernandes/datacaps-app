from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from auth import auth_bp
from views import views_bp
from models import db

app = Flask(__name__)
app.secret_key = 'chave_super_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(views_bp)

# --- ADICIONE ESTE TRECHO ---
with app.app_context():
    db.create_all()
# ----------------------------

if __name__ == '__main__':
    app.run(debug=True)
