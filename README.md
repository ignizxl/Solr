# Configuração do Solr com Docker e API Flask

Este projeto configura o Solr com Docker para indexação de dados, além de implementar uma API Flask para mapear dados de um CSV para um banco de dados PostgreSQL e interagir com o Solr para indexação e consultas.

## 1. **Configuração do Solr com Dockerfile**

### 1.1 **Script `scripts/init-solr.sh`**

Este script é responsável por configurar o Solr no Docker. Ele cria o core desejado e adiciona campos ao schema automaticamente.

#### Descrição do Script

- Inicia o Solr e cria um core se ele não existir.
- Adiciona dois campos ao schema do core: `codigo` e `titulo`.
- Exibe os logs do Solr para monitoramento contínuo.

### 1.2 **Dockerfile**

O Dockerfile configura o Solr utilizando a imagem oficial do Bitnami e executa o script de inicialização (`init-solr.sh`).

#### Comandos para Construir e Executar o Container

```bash
docker build -t solr_cbo .
```

```bash
docker run -d -p 8983:8983 --name solr_cbo solr_cbo
```

---

### 2. **API Flask para Integração com PostgreSQL e Solr**

---

Esta é uma API desenvolvida em Flask para gerenciar documentos, com integração ao banco de dados PostgreSQL e ao mecanismo de busca Apache Solr. A API permite realizar apenas duas operações CRUD (criar e buscar) nos documentos, além de importar dados de um arquivo CSV para o banco e enviar esses dados para o Solr para indexação e busca.

### **2.1 Funcionalidades**

- **CRUD de Documentos:** Criar e buscar documentos armazenados no banco de dados PostgreSQL.

- **Importação de CSV:** Importar documentos de um arquivo CSV para o banco de dados.

- **Envio para Solr:** Enviar documentos armazenados no banco de dados para o Solr para indexação e buscas rápidas.

- **Busca Elástica:**  Realizar consultas flexíveis no Solr usando parâmetros específicos para otimizar os resultados.

A seguir, são apresentados exemplos de como utilizar o endpoint de busca para realizar consultas com a funcionalidade de busca elástica via cURL e diretamente no navegador (Via HTTP).

## Endpoint de Busca

### **GET /api/documentos**
Este endpoint realiza buscas no Solr com base em uma consulta fornecida via parâmetro `q`. A busca utiliza o Solr para realizar uma pesquisa aproximada no título e código dos documentos armazenados no banco de dados.

**Parâmetros**:
- `q` (obrigatório): O termo de busca para consulta no Solr. Este parâmetro é usado para buscar no campo `titulo` do documento.


## Exemplos de busca elástica

### 1. **Busca usando cURL**

Você pode usar o cURL para realizar a consulta diretamente para o endpoint da API.

#### Exemplo 1: Consultar documentos com o termo "General"
```bash
curl -X GET "http://localhost:5000/api/documentos?q=General"
```

#### Exemplo 2: Consultar documentos com múltiplos termos de busca "engenheiro mecatrônico"
```bash
curl -X GET "http://localhost:5000/api/documentos?q=engenheiro%20mecatrônico"
```

Esses comandos irão realizar uma busca no campo titulo do Solr, retornando os documentos correspondentes. O parâmetro q é usado para especificar o termo de busca e, no exemplo acima, o termo de busca é "general" ou múltiplos termos.

##### **Você também pode realizar buscas diretamente no navegador (via HTTP).**

Seguindo os exemplos acima mas, desta vez no seu navegador

> Abra o seu navegador e cole as URLs dos exemplos abaixo 

#### Exemplo 1: Consultar documentos com o termo "General"
```bash
  http://localhost:5000/api/documentos?q=General
```

#### Exemplo 2: Consultar documentos com múltiplos termos de busca "engenheiro mecatrônico" 
```bash
  http://localhost:5000/api/documentos?q=engenheiro mecatrônico
```
> Essas URLs irão fazer uma consulta no Solr e retornar os documentos que correspondem ao termo especificado no parâmetro q.

### **3. Consultas ao Solr (via HTTP)**

**3.1. Consultar por `codigo`**

- **Descrição**: Pesquisa pelo código exato em `codigo`.

  - **Exemplo de consulta**:

    ```bash
    http://localhost:8983/solr/cbo/select?q=codigo:12345&wt=json
    ```

**3.2. Consultar por `titulo`**

- **Descrição**: Pesquisa pelo título exato em `titulo`.

  - **Exemplo de consulta**:

    ```bash
    http://localhost:8983/solr/cbo/select?q=titulo:software&wt=json
    ```

- **Consulta com Wildcard (parcial do título)**

  - **Exemplo**: Busca por títulos que contêm "Eng".

    ```bash
    http://localhost:8983/solr/cbo/select?q=titulo:*Eng*&wt=json
    ```

**3.3. Consultar com múltiplos critérios (`codigo` e `titulo`)**

- **Descrição**: Pesquisa combinada entre `codigo` e `titulo`.
  - **Exemplo de consulta**:
  
    ```bash
    http://localhost:8983/solr/cbo/select?q=codigo:1234 AND titulo:engenheiro&wt=json
    ```

**3.4. Consultar todos os documentos**

- **Descrição**: Retorna todos os documentos no core.
  - **Exemplo de consulta**:

    ```bash
    http://localhost:8983/solr/cbo/select?q=*:*&wt=json
    ```

**3.5. Consultar com filtros**

- **Filtro por `codigo`** (exemplo: `codigo` maior ou igual a 1000):
  
  - **Exemplo de consulta**:

    ```bash
    http://localhost:8983/solr/cbo/select?q=codigo:[1000 TO *]&wt=json
    ```

- **Filtro por `titulo`** (exemplo: títulos que começam com "ana"):
  
  - **Exemplo de consulta**:

    ```bash
    http://localhost:8983/solr/cbo/select?q=titulo:ana*&wt=json
    ```

---

### **4. Enviar dados para o servidor Solr**

Para enviar dados para o Solr, você deve utilizar a URL do core configurado e o endpoint de **update** do Solr. O Solr suporta inserção de dados em formato **JSON** ou **XML** via HTTP POST.

### **Exemplo de URL para Enviar Dados para o Solr**

Se o core estiver configurado com o nome `cbo`, a URL para enviar os dados seria:

```bash
http://localhost:8983/solr/cbo/update?commit=true
```

- **`/update`**: Endpoint que permite a inserção de dados no Solr.
- **`?commit=true`**: Parâmetro que faz o commit (salvamento) dos dados imediatamente após a inserção.

#### **Exemplo de Dados JSON para Inserção**

```json
[
  {
    "id": 1,
    "codigo": "12345",
    "titulo": "Engenheiro de Software"
  },
  {
    "id": 2,
    "codigo": "67890",
    "titulo": "Analista de Sistemas"
  }
]
```

---

### **Dependências**

Este projeto depende das seguintes tecnologias e bibliotecas:

- **Solr**: Para indexação e pesquisa de dados.
- **Docker**: Para criar o container do Solr.
- **Flask**: Para a API que interage com o banco de dados e o Solr.
- **PostgreSQL**: Para o banco de dados onde os dados são armazenados.

---

### **Desenvolvedores**

Este projeto foi desenvolvido por:

- **[João Igor](https://github.com/ignizxl)**
- **[Natália Gomes](https://github.com/nataliatsi)**
