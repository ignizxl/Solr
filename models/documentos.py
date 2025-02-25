from flask_restful import fields
from helpers.database import db  # Importa a instância db

# Definindo o esquema de saída para Documento
documento_fields = {
  'id': fields.Integer,
  'codigo': fields.String,
  'titulo': fields.String
}

# Modelo do Documento
class DocumentoModel(db.Model):
  """
  Modelo para a tabela 'documentos' no banco de dados.
  """
  __tablename__ = 'documentos'

  id = db.Column(db.Integer, primary_key=True)  # Chave primária
  codigo = db.Column(db.String(50), nullable=False)  # Código do documento
  titulo = db.Column(db.String(255), nullable=False)  # Título do documento

  def __repr__(self):
    """Retorna a representação textual do objeto."""
    return f"Documento(codigo={self.codigo}, titulo={self.titulo})"

  def json(self):
    """Converte o objeto em um dicionário JSON."""
    return {
      'id': self.id,
      'codigo': self.codigo,
      'titulo': self.titulo
      }
