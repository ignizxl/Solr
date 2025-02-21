from flask_restful import Api
from resources.documentos import Documento

# Criando a instância da API com prefixo '/api'
api = Api(prefix="/api")

# Definindo as rotas da API
api.add_resource(Documento, 
    '/documentos', 
)