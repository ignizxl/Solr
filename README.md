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
