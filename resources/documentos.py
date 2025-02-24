import csv
import json
import requests
from flask import request
from flask_restful import Resource, marshal_with
from models.documentos import DocumentoModel, db, documento_fields


class Documento(Resource):
    """
    Métodos GET, POST.
    """

    def get(self):
        query = request.args.get("q", "")  # pega o parâmetro "q" da URL
        if not query:
            return {"message": "Consulta não pode estar vazia"}, 400

        url_solr = "http://solr:8983/solr/cbo/select"
        params = {
            "q": f"titulo:{query}~",
            "rows": 10,
            "defType": "edismax",  # parser edismax para melhorar a relevância
            "qf": "titulo codigo",
            "wt": "json",
        }

        try:
            # faz a consulta no Solr
            response = requests.get(url_solr, params=params)
            if response.status_code == 200:
                return (
                    response.json()["response"]["docs"],
                    200,
                )  # se deu certo, retorna os documentos
            else:
                return {
                    "message": "Erro ao buscar dados no Solr",
                    "details": response.text,
                }, response.status_code
        except requests.exceptions.RequestException as e:
            return {"message": f"Erro de conexão com o Solr: {str(e)}"}, 500

    @marshal_with(documento_fields)
    def post(self):
        dados = request.get_json()
        if not (dados.get("codigo") and dados.get("titulo")):
            return {"message": "Código e título são obrigatórios"}, 400

        novo_documento = DocumentoModel(codigo=dados["codigo"], titulo=dados["titulo"])
        db.session.add(novo_documento)
        db.session.commit()
        return novo_documento, 201

    @staticmethod
    def importar_csv(path):
        """Função para importar dados do CSV para o banco de dados."""
        try:
            with open(path, "r", encoding="ISO-8859-1") as file:
                reader = csv.DictReader(file, delimiter=";")

                count = 0
                for row in reader:
                    print(f"Linha lida do CSV: {row}")
                    if "CODIGO" in row and "TITULO" in row:
                        documento = DocumentoModel(
                            codigo=row["CODIGO"], titulo=row["TITULO"]
                        )
                        db.session.add(documento)
                        print(
                            f"Documento adicionado: {row['CODIGO']} - {row['TITULO']}"
                        )
                        count += 1
                db.session.commit()
                print(
                    f"Importação concluída com sucesso. {count} documentos processados."
                )
        except Exception as e:
            print(f"Erro ao processar o arquivo CSV: {str(e)}")

    def enviar_solr(self):
        """Consulta os documentos no banco e envia para o Solr via POST."""

        url_solr = "http://solr:8983/solr/cbo/update?commitWithin=5000"
        documentos = DocumentoModel.query.all()
        if not documentos:
            return {"message": "Nenhum documento encontrado para enviar ao Solr"}, 400

        # converte pra json
        dados_para_solr = [
            {"id": str(doc.id), "codigo": doc.codigo, "titulo": doc.titulo}
            for doc in documentos
        ]
        print(
            "Enviando os seguintes dados para o Solr:",
            json.dumps(dados_para_solr, indent=4),
        )

        try:
            response = requests.post(
                url_solr,
                json=dados_para_solr,
                headers={"Content-Type": "application/json"},
            )
            print("Resposta do Solr:", response.status_code, response.text)

            if response.status_code == 200:
                return {"message": "Dados enviados ao Solr com sucesso"}, 200
            else:
                return {
                    "message": "Erro ao enviar os dados para o Solr",
                    "details": response.text,
                }, response.status_code

        except requests.exceptions.RequestException as e:
            return {"message": f"Erro de conexão com o Solr: {str(e)}"}, 500


class SolrSync(Resource):
    def post(self):
        documento = Documento()
        return documento.enviar_solr()
