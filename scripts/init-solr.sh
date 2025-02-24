#!/bin/bash
set -e

core_name="cbo"
solr_url="http://localhost:8983/solr"

echo "🕒 Aguardando o Solr iniciar..."
solr start
sleep 5
echo "✅ Solr iniciado!"

if curl -s "${solr_url}/admin/cores?action=STATUS" | grep -q "\"${core_name}\""; then
    echo "🟢 Core '${core_name}' já existe."
else
    echo "⚙️ Criando core '${core_name}'..."
    solr create -c "${core_name}"
    echo "✅ Core '${core_name}' criado!"
fi

sleep 5

# Adicionar campos ao schema após a criação do core
echo "Adicionando campos ao schema do core '${core_name}'..."

curl -X POST -H "Content-Type: application/json" \
    --data '{
      "add-field": {
        "name": "codigo",
        "type": "string",
        "indexed": true,
        "stored": true
      }
    }' \
    "${solr_url}/${core_name}/schema"

curl -X POST -H "Content-Type: application/json" \
    --data '{
      "add-field": {
        "name": "titulo",
        "type": "text_general",
        "indexed": true,
        "stored": true
      }
    }' \
    "${solr_url}/${core_name}/schema"

echo "Campos 'codigo' e 'titulo' adicionados com sucesso ao schema!"

tail -f /opt/bitnami/solr/logs/solr.log
