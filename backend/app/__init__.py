import os
from flask import Flask,jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_login import LoginManager
from .config import Config

mysql = MySQL()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    mysql.init_app(app)
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
    from .routes import api  
    app.register_blueprint(api)
    login_manager.login_view = 'api.get_data'  # nombre de la función de tu ruta de login
    login_manager.init_app(app)

    return app


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'message': 'No autorizado'}), 401

@login_manager.user_loader
def load_user(user_id):
    from .models import obtener_usuario_por_id
    print(f"Cargando usuario con ID: {user_id}")
    return obtener_usuario_por_id(user_id)
# Esto permite: from app import mysql
globals()['mysql'] = mysql
