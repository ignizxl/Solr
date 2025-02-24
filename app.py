from flask import Flask
from helpers.database import db
from helpers.cors import cors
from helpers.api import api
from resources.documentos import Documento

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://admin:admin@postgres:5432/solr_cbo"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializando extensões
db.init_app(app)
cors.init_app(app)
api.init_app(app)

# Criando as tabelas
with app.app_context():
    db.drop_all()
    db.create_all()

with app.app_context():
    csv_path = "./ocupacao.csv"
    Documento.importar_csv(csv_path)
    Documento().enviar_solr()

if __name__ == "__main__":
    app.run(debug=True)
