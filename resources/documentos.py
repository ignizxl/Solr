from flask import request
from flask_restful import Resource, marshal_with
from models.documentos import DocumentoModel, db, documento_fields

class Documento(Resource):
    """
    Recurso para gerenciar os documentos.
    Implementa os métodos GET e POST.
    """
    
    @marshal_with(documento_fields)
    def get(self, documento_id=None):
        if documento_id:
            documento = DocumentoModel.query.filter_by(id=documento_id).first()
            if documento:
                return documento, 200
            return {'message': 'Documento não encontrado'}, 404
        else:
            documentos = DocumentoModel.query.all()
            return documentos, 200

    @marshal_with(documento_fields)
    def post(self):
        dados = request.get_json()
        if not (dados.get('codigo') and dados.get('titulo')):
          return {'message': 'Código e título são obrigatórios'}, 400

        novo_documento = DocumentoModel(
            codigo=dados['codigo'],
            titulo=dados['titulo']
        )
        db.session.add(novo_documento)
        db.session.commit()
        return novo_documento, 201