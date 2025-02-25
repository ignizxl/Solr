from flask_restful import Api
from resources.documentos import Documento, SolrSync

# Criando a instância da API com prefixo '/api'
api = Api(prefix="/api")

# Definindo as rotas da API
api.add_resource(Documento, 
    '/documentos', 
    '/documentos/<int:documento_id>', 
    '/documentos/exportar_json', 
    '/documentos/enviar_para_solr'
)
api.add_resource(SolrSync, '/documentos/sync_solr')