from flask_restful import Api
from flask import Flask

# Importando os recursos
from resources.documentos import Documento

# Criando a aplicação Flask
app = Flask(__name__)

# Inicializando a API com o prefixo '/api'
api = Api(app, prefix="/api")

# Definindo as rotas da API
api.add_resource(Documento, '/documentos', '/documentos/<int:documento_id>')