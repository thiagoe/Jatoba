# API Jatobá - Gerenciamento de Equipamentos, Fabricantes e Arquivos

---

## 📄 Descrição do Projeto

A API Jatobá é um backend robusto e flexível, construído com **Flask** e **PyMySQL**, projetado para gerenciar informações sobre **fabricantes**, **equipamentos** e **arquivos** (como firmwares e documentos). Ela oferece funcionalidades CRUD (Criar, Ler, Atualizar, Deletar) para essas entidades, além de recursos de busca global, upload/download de arquivos e estatísticas administrativas.

O objetivo principal desta API é fornecer uma base sólida para sistemas de gerenciamento de ativos, permitindo o registro, a organização e a recuperação eficiente de dados relacionados a hardware e seus componentes de software/documentação.

## ✨ Funcionalidades Principais

* **Gerenciamento de Fabricantes**: Adicione, liste, atualize e remova fabricantes, com suporte para upload de logos.
* **Gerenciamento de Equipamentos**: Adicione, liste, atualize e remova equipamentos, com associação a fabricantes e upload de imagens.
* **Gerenciamento de Arquivos**: Faça upload, liste, atualize metadados e gerencie downloads de firmwares e documentos, associando-os a equipamentos.
* **Funcionalidades de Busca**: Busque por fabricantes e equipamentos usando termos específicos.
* **Estatísticas Administrativas**: Obtenha insights sobre os dados armazenados na API.
* **Sistema de Logging Detalhado**: Logs configuráveis para monitoramento e depuração, salvos em arquivo e exibidos no console.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Flask**: Micro-framework web para Python.
* **PyMySQL**: Driver nativo Python para MySQL/MariaDB.
* **python-dotenv**: Para gerenciar variáveis de ambiente.

## 🚀 Como Configurar e Rodar

Siga estes passos para configurar e executar a API localmente.

### Pré-requisitos

* **Python 3.x** instalado.
* Um servidor de banco de dados **MariaDB** ou **MySQL** em execução.

### 1. Clonar o Repositório

```bash
git clone [https://github.com/seu-usuario/api-jatoba.git](https://github.com/seu-usuario/api-jatoba.git) # Substitua pelo seu link do repositório
cd api-jatoba
```

## 2. Criar e Ativar o Ambiente Virtual
É uma boa prática usar um ambiente virtual para gerenciar as dependências.



''''python3 -m venv venv
''''source venv/bin/activate # No Linux/macOS
''''venv\Scripts\activate # No Windows

# 3. Instalar as Dependências

```Bash

'' pip install -r requirements.txt
```
# 4. Configurar Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto e configure as variáveis de ambiente necessárias para a conexão com o banco de dados e a pasta de uploads.

Exemplo de .env:

```Bash

DB_HOST=localhost
DB_PORT=3306
DB_USER=seu_usuario_db
DB_PASSWORD=sua_senha_db
DB_NAME=api_jatoba_db
UPLOAD_FOLDER=./uploads
LOG_LEVEL=INFO
```

DB_HOST: Endereço do seu servidor de banco de dados.

DB_PORT: Porta do seu banco de dados (geralmente 3306).

DB_USER: Nome de usuário do banco de dados.

DB_PASSWORD: Senha do banco de dados.

DB_NAME: Nome do banco de dados que será utilizado pela API.

UPLOAD_FOLDER: Caminho para a pasta onde os arquivos serão armazenados.

LOG_LEVEL: Nível de detalhe dos logs (DEBUG, INFO, WARNING, ERROR, CRITICAL).

# 5. Configurar o Banco de Dados
Crie o banco de dados e as tabelas necessárias. Você pode usar um cliente MySQL/MariaDB (como DBeaver, MySQL Workbench, ou o terminal mysql).

``` Bash
SQL

CREATE DATABASE IF NOT EXISTS api_jatoba_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE api_jatoba_db;

CREATE TABLE IF NOT EXISTS fabricantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    logo_url VARCHAR(512),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS equipamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    manufacturer_id INT,
    image_url VARCHAR(512),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (manufacturer_id) REFERENCES fabricantes(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS arquivos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type ENUM('firmware', 'document') NOT NULL,
    equipment_id INT,
    file_url VARCHAR(512) NOT NULL,
    file_size BIGINT,
    download_count INT DEFAULT 0,
    uploaded_by INT, -- Pode ser um ID de usuário, se houver um sistema de usuários
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES equipamentos(id) ON DELETE SET NULL
);

-- Opcional: Tabela de usuários, se você for implementar autenticação
-- CREATE TABLE IF NOT EXISTS users (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     username VARCHAR(255) NOT NULL UNIQUE,
--     password_hash VARCHAR(255) NOT NULL,
--     email VARCHAR(255) UNIQUE,
--     role ENUM('admin', 'user') DEFAULT 'user',
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

```

# 6. Rodar a Aplicação Flask
``` Bash

python app.py
```
A API estará rodando em http://127.0.0.1:5000.

🖥️ Endpoints da API
Você pode testar os endpoints usando ferramentas como curl (terminal), Postman, Insomnia ou diretamente pelo navegador para requisições GET.

Endpoints Gerais (/)
GET /

Descrição: Verifica o status da API.

curl http://127.0.0.1:5000/

POST /upload

Descrição: Faz o upload de um arquivo genérico para a pasta uploads.

curl -X POST -F "file=@/caminho/para/seu/arquivo.txt" http://127.0.0.1:5000/upload

DELETE /upload/<filename>

Descrição: Deleta um arquivo genérico da pasta uploads.

curl -X DELETE http://127.0.0.1:5000/upload/nome_do_arquivo.txt

Endpoints de Fabricantes (/manufacturers)
GET /manufacturers/

Descrição: Lista todos os fabricantes.

curl http://127.0.0.1:5000/manufacturers/

GET /manufacturers/<id>

Descrição: Obtém um fabricante pelo ID.

curl http://127.0.0.1:5000/manufacturers/1

POST /manufacturers/

Descrição: Cria um novo fabricante.

curl -X POST -H "Content-Type: application/json" -d '{"name": "Nova Indústria", "logo_url": "http://example.com/logo_nova.png"}' http://127.0.0.1:5000/manufacturers/

PUT /manufacturers/<id>

Descrição: Atualiza um fabricante existente.

curl -X PUT -H "Content-Type: application/json" -d '{"name": "Nova Indústria Atualizada", "logo_url": "http://example.com/logo_atualizada.png"}' http://127.0.0.1:5000/manufacturers/1

DELETE /manufacturers/<id>

Descrição: Exclui um fabricante.

curl -X DELETE http://127.0.0.1:5000/manufacturers/1

POST /manufacturers/<id>/logo

Descrição: Faz o upload de um logo para um fabricante.

curl -X POST -F "logo=@/caminho/para/seu/logo.png" http://127.0.0.1:5000/manufacturers/1/logo

Endpoints de Equipamentos (/equipments)
GET /equipments/

Descrição: Lista todos os equipamentos.

curl http://127.0.0.1:5000/equipments/

GET /equipments/?manufacturer_id=<id>

Descrição: Lista equipamentos filtrados por ID de fabricante.

curl http://127.0.0.1:5000/equipments/?manufacturer_id=1

GET /equipments/<id>

Descrição: Obtém um equipamento pelo ID.

curl http://127.0.0.1:5000/equipments/1

POST /equipments/

Descrição: Cria um novo equipamento.

curl -X POST -H "Content-Type: application/json" -d '{"name": "Máquina XYZ", "model": "V3.0", "manufacturer_id": 1, "image_url": "http://example.com/equipamento_xyz.jpg"}' http://127.0.0.1:5000/equipments/

PUT /equipments/<id>

Descrição: Atualiza um equipamento existente.

curl -X PUT -H "Content-Type: application/json" -d '{"name": "Máquina XYZ Pro", "model": "V3.1", "manufacturer_id": 1, "image_url": "http://example.com/equipamento_xyz_pro.jpg"}' http://127.0.0.1:5000/equipments/1

DELETE /equipments/<id>

Descrição: Exclui um equipamento.

curl -X DELETE http://127.0.0.1:5000/equipments/1

POST /equipments/<id>/image

Descrição: Faz o upload de uma imagem para um equipamento.

curl -X POST -F "image=@/caminho/para/sua/imagem.jpg" http://127.0.0.1:5000/equipments/1/image

Endpoints de Arquivos (/files)
GET /files/

Descrição: Lista todos os arquivos.

curl http://127.0.0.1:5000/files/

GET /files/?type=<type>

Descrição: Lista arquivos filtrados por tipo (firmware ou document).

curl http://127.0.0.1:5000/files/?type=firmware

GET /files/?equipment_id=<id>

Descrição: Lista arquivos filtrados por ID de equipamento.

curl http://127.0.0.1:5000/files/?equipment_id=1

GET /files/<id>

Descrição: Obtém metadados de um arquivo pelo ID.

curl http://127.0.0.1:5000/files/1

POST /files/

Descrição: Faz o upload de um novo arquivo e salva seus metadados.

curl -X POST -F "file=@/caminho/para/seu/firmware.bin" -F "name=Firmware v1.0" -F "type=firmware" -F "equipment_id=1" -F "uploaded_by=101" http://127.0.0.1:5000/files/

PUT /files/<id>

Descrição: Atualiza os metadados de um arquivo existente.

curl -X PUT -H "Content-Type: application/json" -d '{"name": "Firmware v1.1 Atualizado", "type": "firmware"}' http://127.0.0.1:5000/files/1

DELETE /files/<id>

Descrição: Exclui um arquivo (registro e físico).

curl -X DELETE http://127.0.0.1:5000/files/1

GET /files/<id>/download

Descrição: Baixa um arquivo.

curl -O -J http://127.0.0.1:5000/files/1/download

POST /files/<id>/download

Descrição: Incrementa o contador de downloads de um arquivo.

curl -X POST http://127.0.0.1:5000/files/1/download

Endpoints de Busca (/search)
GET /search/?q=<query>

Descrição: Realiza busca global em fabricantes e equipamentos.

curl http://127.0.0.1:5000/search/?q=termo

GET /search/manufacturers?q=<query>

Descrição: Busca fabricantes pelo nome.

curl http://127.0.0.1:5000/search/manufacturers?q=termo

GET /search/equipments?q=<query>

Descrição: Busca equipamentos pelo nome ou modelo.

curl http://127.0.0.1:5000/search/equipments?q=termo

Endpoints de Administração (/admin)
GET /admin/stats

Descrição: Obtém estatísticas gerais do sistema.

curl http://127.0.0.1:5000/admin/stats

GET /admin/users

Descrição: (Placeholder) Lista usuários.

curl http://127.0.0.1:5000/admin/users

PUT /admin/users/<id>

Descrição: (Placeholder) Atualiza um usuário.

curl -X PUT -H "Content-Type: application/json" -d '{"username": "novo_usuario"}' http://127.0.0.1:5000/admin/users/1

DELETE /admin/users/<id>

Descrição: (Placeholder) Exclui um usuário.

curl -X DELETE http://127.0.0.1:5000/admin/users/1
