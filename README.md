# Configuração do Solr com Docker e API Flask

Este projeto usa Docker Compose para configurar os serviços necessários para a aplicação: API Flask, PostgreSQL e Solr. A API Flask mapeia os dados de um CSV para o banco de dados PostgreSQL e, em seguida, coleta todos os dados, os organiza em um JSON e os envia para o Solr para indexação e consultas.

Os serviços são definidos em um arquivo `docker-compose.yml`, com a configuração de redes, containers e variáveis de ambiente. O Solr é iniciado com um script de inicialização, enquanto o PostgreSQL armazena os dados.

---

### **Comandos Docker Compose**

- **Executar Docker Compose em Background:**

  Para rodar os serviços definidos no `docker-compose.yml` em segundo plano (modo detached), use o seguinte comando:
  
  ```bash
  docker-compose up -d
  ```

- **Rebuild dos Containers (se o Compose não funcionar corretamente):**

  Caso o Docker Compose não esteja funcionando como esperado, execute o comando abaixo para reconstruir os containers e garantir que tudo esteja configurado corretamente:
  
  ```bash
  docker-compose up --build -d
  ```

- **Parar os serviços com Docker Compose:**

  Para parar os serviços em execução, execute:
  
  ```bash
  docker-compose down
  ```

- **Excluir volumes ao parar os serviços:**

  Para remover os volumes, utilize o comando abaixo:
  
  ```bash
  docker-compose down -v
  ```

---

Aqui está a versão reescrita de forma mais coesa e coerente:

### 2. **API Flask**

Esta API foi desenvolvida em Flask para gerenciar documentos, com integração ao banco de dados PostgreSQL e ao mecanismo de busca Apache Solr. Ela oferece operações básicas de CRUD (criar e buscar) para os documentos, além de permitir a importação de dados de um arquivo CSV para o banco de dados e o envio desses dados ao Solr para indexação e busca eficiente.

#### **2.1 Funcionalidades**

- **CRUD de Documentos:** Permite a criação e a busca de documentos armazenados no banco de dados PostgreSQL.

- **Importação de CSV:** Facilita a importação de documentos de um arquivo CSV para o banco de dados PostgreSQL.

- **Envio para Solr:** Envia os documentos armazenados no banco de dados para o Solr, realizando a indexação para buscas rápidas.

- **Busca Elástica:** Permite realizar consultas flexíveis no Solr, utilizando parâmetros específicos para otimizar os resultados.

A seguir, são apresentados exemplos de como utilizar o endpoint de busca para consultas, tanto via cURL quanto diretamente no navegador (via HTTP).

#### **2.2 Endpoint de Busca**

O endpoint de busca permite realizar buscas nos documentos armazenados no banco de dados PostgreSQL e indexados no Solr. A pesquisa é realizada com base em uma consulta fornecida via parâmetro `q`, que é usado para buscar no campo `titulo` e `codigo` dos documentos.

**Parâmetros**:

- `q` (obrigatório): O termo de busca que será utilizado para procurar nos campos `titulo` e `codigo` dos documentos.

#### **2.3 Exemplos de Consultas HTTP**

##### 1. **Consulta utilizando cURL**

Você pode utilizar o cURL para fazer uma requisição GET diretamente ao endpoint da API.

- **Exemplo 1:** Buscar documentos com o termo "General"
  
  ```bash
  curl -X GET "http://localhost:5000/api/documentos?q=General"
  ```

- **Exemplo 2:** Buscar documentos com múltiplos termos, como "engenheiro mecatrônico"
  
  ```bash
  curl -X GET "http://localhost:5000/api/documentos?q=engenheiro%20mecatrônico"
  ```

##### 2. **Consulta via Navegador (HTTP)**

Você também pode fazer a busca diretamente no navegador acessando a URL correspondente, por exemplo:

- **Exemplo 1:** Buscar documentos com o termo "General"
  
  ```bash
  http://localhost:5000/api/documentos?q=General
  ```

- **Exemplo 2:** Buscar documentos com o termo "engenheiro mecatrônico"
  
  ```bash
  http://localhost:5000/api/documentos?q=engenheiro%20mecatrônico
  ```

Esses comandos irão realizar uma busca no campo titulo do Solr, retornando os documentos correspondentes. O parâmetro q é usado para especificar o termo de busca e, no exemplo acima, o termo de busca é "general" ou múltiplos termos.

---

### **Dependências**

Este projeto depende das seguintes tecnologias e bibliotecas:

- **[Solr](https://hub.docker.com/r/bitnami/solr)**: Para indexação e pesquisa de dados.
- **[Docker](https://www.docker.com/)**: Para criar o container do Solr.
- **[Flask](https://flask-restful.readthedocs.io/en/latest/)**: Para a API que interage com o banco de dados e o Solr.
- **[PostgreSQL](https://www.postgresql.org/)**: Para o banco de dados onde os dados são armazenados.

---

### **Desenvolvedores**

Este projeto foi desenvolvido por:

- **[João Igor](https://github.com/ignizxl)**
- **[Natália Gomes](https://github.com/nataliatsi)**
