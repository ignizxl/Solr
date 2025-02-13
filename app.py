from flask import Flask
from flask_restful import Api
from helpers.database import db
from helpers.cors import cors
from resources.documentos import Documento

# Inicializando a aplicação Flask
app = Flask(__name__)

# Configurando a API
api = Api(app)

# Configurando o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o SQLAlchemy com o app
db.init_app(app)

# Inicializando o CORS com o app
cors.init_app(app)

# Criando as tabelas 
with app.app_context():
    db.create_all()  # Criar as tabelas

# Definindo as rotas da API
api.add_resource(Documento, '/documentos', '/documentos/<int:documento_id>')

if __name__ == '__main__':
    app.run(debug=True)