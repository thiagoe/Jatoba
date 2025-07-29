<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>README - API Jatobá</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 20px auto;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
            margin-top: 30px;
        }
        h1 {
            border-bottom: 3px solid #3498db;
        }
        pre {
            background-color: #ecf0f1;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            white-space: pre-wrap; /* Permite quebras de linha em textos longos */
            word-wrap: break-word; /* Quebra palavras longas */
        }
        code {
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            background-color: #e0e6eb;
            padding: 2px 4px;
            border-radius: 3px;
            color: #c0392b; /* Cor para código inline */
        }
        pre code {
            background-color: transparent;
            padding: 0;
            color: #2c3e50; /* Cor para código em blocos */
        }
        ul {
            list-style-type: disc;
            margin-left: 20px;
        }
        strong {
            color: #34495e;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>API Jatobá - Gerenciamento de Equipamentos, Fabricantes e Arquivos</h1>

    <hr>

    <h2>📄 Descrição do Projeto</h2>
    <p>A API Jatobá é um backend robusto e flexível, construído com <b>Flask</b> e <b>PyMySQL</b>, projetado para gerenciar informações sobre <b>fabricantes</b>, <b>equipamentos</b> e <b>arquivos</b> (como firmwares e documentos). Ele oferece funcionalidades CRUD (Criar, Ler, Atualizar, Deletar) para essas entidades, além de recursos de busca global, upload/download de arquivos e estatísticas administrativas.</p>
    <p>O objetivo principal desta API é fornecer uma base sólida para sistemas de gerenciamento de ativos, permitindo o registro, a organização e a recuperação eficiente de dados relacionados a hardware e seus componentes de software/documentação.</p>

    <h2>✨ Funcionalidades Principais</h2>
    <ul>
        <li><b>Gerenciamento de Fabricantes</b>: Adicione, liste, atualize e remova fabricantes, com suporte para upload de logos.</li>
        <li><b>Gerenciamento de Equipamentos</b>: Adicione, liste, atualize e remova equipamentos, com associação a fabricantes e upload de imagens.</li>
        <li><b>Gerenciamento de Arquivos</b>: Faça upload, liste, atualize metadados e gerencie downloads de firmwares e documentos, associando-os a equipamentos.</li>
        <li><b>Funcionalidades de Busca</b>: Busque por fabricantes e equipamentos usando termos específicos.</li>
        <li><b>Estatísticas Administrativas</b>: Obtenha insights sobre os dados armazenados na API.</li>
        <li><b>Sistema de Logging Detalhado</b>: Logs configuráveis para monitoramento e depuração, salvos em arquivo e exibidos no console.</li>
    </ul>

    <h2>🛠️ Tecnologias Utilizadas</h2>
    <ul>
        <li><b>Python 3.x</b></li>
        <li><b>Flask</b>: Micro-framework web para Python.</li>
        <li><b>PyMySQL</b>: Driver nativo Python para MySQL/MariaDB.</li>
        <li><b>python-dotenv</b>: Para gerenciar variáveis de ambiente.</li>
    </ul>

    <h2>🚀 Como Configurar e Rodar</h2>
    <p>Siga estes passos para configurar e executar a API localmente.</p>

    <h3>Pré-requisitos</h3>
    <ul>
        <li><b>Python 3.x</b> instalado.</li>
        <li>Um servidor de banco de dados <b>MariaDB</b> ou <b>MySQL</b> em execução.</li>
    </ul>

    <h3>1. Clonar o Repositório</h3>
    <pre><code>git clone https://github.com/seu-usuario/api-jatoba.git # Substitua pelo seu link do repositório
cd api-jatoba</code></pre>

    <h3>2. Criar e Ativar o Ambiente Virtual</h3>
    <p>É uma boa prática usar um ambiente virtual para gerenciar as dependências.</p>
    <pre><code>python3 -m venv venv
source venv/bin/activate # No Linux/macOS
# venv\Scripts\activate # No Windows</code></pre>

    <h3>3. Instalar as Dependências</h3>
    <pre><code>pip install -r requirements.txt</code></pre>

    <h3>4. Configurar Variáveis de Ambiente</h3>
    <p>Crie um arquivo <code>.env</code> na raiz do projeto e configure as variáveis de ambiente necessárias para a conexão com o banco de dados e a pasta de uploads.</p>
    <p>Exemplo de <code>.env</code>:</p>
    <pre><code>DB_HOST=localhost
DB_PORT=3306
DB_USER=seu_usuario_db
DB_PASSWORD=sua_senha_db
DB_NAME=api_jatoba_db
UPLOAD_FOLDER=./uploads
LOG_LEVEL=INFO</code></pre>
    <ul>
        <li><b><code>DB_HOST</code></b>: Endereço do seu servidor de banco de dados.</li>
        <li><b><code>DB_PORT</code></b>: Porta do seu banco de dados (geralmente 3306).</li>
        <li><b><code>DB_USER</code></b>: Nome de usuário do banco de dados.</li>
        <li><b><code>DB_PASSWORD</code></b>: Senha do banco de dados.</li>
        <li><b><code>DB_NAME</code></b>: Nome do banco de dados que será utilizado pela API.</li>
        <li><b><code>UPLOAD_FOLDER</code></b>: Caminho para a pasta onde os arquivos serão armazenados.</li>
        <li><b><code>LOG_LEVEL</code></b>: Nível de detalhe dos logs (DEBUG, INFO, WARNING, ERROR, CRITICAL).</li>
    </ul>

    <h3>5. Configurar o Banco de Dados</h3>
    <p>Crie o banco de dados e as tabelas necessárias. Você pode usar um cliente MySQL/MariaDB (como DBeaver, MySQL Workbench, ou o terminal <code>mysql</code>).</p>
    <pre><code>CREATE DATABASE IF NOT EXISTS api_jatoba_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

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
    uploaded_by INT,
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
-- );</code></pre>

    <h3>6. Rodar a Aplicação Flask</h3>
    <pre><code>python app.py</code></pre>
    <p>A API estará rodando em <code>http://127.0.0.1:5000</code>.</p>

    <h2>🖥️ Endpoints da API</h2>
    <p>Você pode testar os endpoints usando ferramentas como <code>curl</code> (terminal), Postman, Insomnia ou diretamente pelo navegador para requisições GET.</p>

    <h3>Endpoints Gerais (<code>/</code>)</h3>
    <ul>
        <li><b><code>GET /</code></b>
            <ul>
                <li><b>Descrição</b>: Verifica o status da API.</li>
                <li><code>curl http://127.0.0.1:5000/</code></li>
            </ul>
        </li>
        <li><b><code>POST /upload</code></b>
            <ul>
                <li><b>Descrição</b>: Faz o upload de um arquivo genérico para a pasta <code>uploads</code>.</li>
                <li><code>curl -X POST -F "file=@/caminho/para/seu/arquivo.txt" http://127.0.0.1:5000/upload</code></li>
            </ul>
        </li>
        <li><b><code>DELETE /upload/&lt;filename&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Deleta um arquivo genérico da pasta <code>uploads</code>.</li>
                <li><code>curl -X DELETE http://127.0.0.1:5000/upload/nome_do_arquivo.txt</code></li>
            </ul>
        </li>
    </ul>

    <h3>Endpoints de Fabricantes (<code>/manufacturers</code>)</h3>
    <ul>
        <li><b><code>GET /manufacturers/</code></b>
            <ul>
                <li><b>Descrição</b>: Lista todos os fabricantes.</li>
                <li><code>curl http://127.0.0.1:5000/manufacturers/</code></li>
            </ul>
        </li>
        <li><b><code>GET /manufacturers/&lt;id&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Obtém um fabricante pelo ID.</li>
                <li><code>curl http://127.0.0.1:5000/manufacturers/1</code></li>
            </ul>
        </li>
        <li><b><code>POST /manufacturers/</code></b>
            <ul>
                <li><b>Descrição</b>: Cria um novo fabricante.</li>
                <li><code>curl -X POST -H "Content-Type: application/json" -d '{"name": "Nova Indústria", "logo_url": "http://example.com/logo_nova.png"}' http://127.0.0.1:5000/manufacturers/</code></li>
            </ul>
        </li>
        <li><b><code>PUT /manufacturers/&lt;id&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Atualiza um fabricante existente.</li>
                <li><code>curl -X PUT -H "Content-Type: application/json" -d '{"name": "Nova Indústria Atualizada", "logo_url": "http://example.com/logo_atualizada.png"}' http://127.0.0.1:5000/manufacturers/1</code></li>
            </ul>
        </li>
        <li><b><code>DELETE /manufacturers/&lt;id&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Exclui um fabricante.</li>
                <li><code>curl -X DELETE http://127.0.0.1:5000/manufacturers/1</code></li>
            </ul>
        </li>
        <li><b><code>POST /manufacturers/&lt;id&gt;/logo</code></b>
            <ul>
                <li><b>Descrição</b>: Faz o upload de um logo para um fabricante.</li>
                <li><code>curl -X POST -F "logo=@/caminho/para/seu/logo.png" http://127.0.0.1:5000/manufacturers/1/logo</code></li>
            </ul>
        </li>
    </ul>

    <h3>Endpoints de Equipamentos (<code>/equipments</code>)</h3>
    <ul>
        <li><b><code>GET /equipments/</code></b>
            <ul>
                <li><b>Descrição</b>: Lista todos os equipamentos.</li>
                <li><code>curl http://127.0.0.1:5000/equipments/</code></li>
            </ul>
        </li>
        <li><b><code>GET /equipments/?manufacturer_id=&lt;id&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Lista equipamentos filtrados por ID de fabricante.</li>
                <li><code>curl http://127.0.0.1:5000/equipments/?manufacturer_id=1</code></li>
            </ul>
        </li>
        <li><b><code>GET /equipments/&lt;id&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Obtém um equipamento pelo ID.</li>
                <li><code>curl http://127.0.0.1:5000/equipments/1</code></li>
            </ul>
        </li>
        <li><b><code>POST /equipments/</code></b>
            <ul>
                <li><b>Descrição</b>: Cria um novo equipamento.</li>
                <li><code>curl -X POST -H "Content-Type: application/json" -d '{"name": "Máquina XYZ", "model": "V3.0", "manufacturer_id": 1, "image_url": "http://example.com/equipamento_xyz.jpg"}' http://127.0.0.1:5000/equipments/</code></li>
            </ul>
        </li>
        <li><b><code>PUT /equipments/&lt;id&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Atualiza um equipamento existente.</li>
                <li><code>curl -X PUT -H "Content-Type: application/json" -d '{"name": "Máquina XYZ Pro", "model": "V3.1", "manufacturer_id": 1, "image_url": "http://example.com/equipamento_xyz_pro.jpg"}' http://127.0.0.1:5000/equipments/1</code></li>
            </ul>
        </li>
        <li><b><code>DELETE /equipments/&lt;id&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Exclui um equipamento.</li>
                <li><code>curl -X DELETE http://127.0.0.1:5000/equipments/1</code></li>
            </ul>
        </li>
        <li><b><code>POST /equipments/&lt;id&gt;/image</code></b>
            <ul>
                <li><b>Descrição</b>: Faz o upload de uma imagem para um equipamento.</li>
                <li><code>curl -X POST -F "image=@/caminho/para/sua/imagem.jpg" http://127.0.0.1:5000/equipments/1/image</code></li>
            </ul>
        </li>
    </ul>

    <h3>Endpoints de Arquivos (<code>/files</code>)</h3>
    <ul>
        <li><b><code>GET /files/</code></b>
            <ul>
                <li><b>Descrição</b>: Lista todos os arquivos.</li>
                <li><code>curl http://127.0.0.1:5000/files/</code></li>
            </ul>
        </li>
        <li><b><code>GET /files/?type=&lt;type&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Lista arquivos filtrados por tipo (<code>firmware</code> ou <code>document</code>).</li>
                <li><code>curl http://127.0.0.1:5000/files/?type=firmware</code></li>
            </ul>
        </li>
        <li><b><code>GET /files/?equipment_id=&lt;id&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Lista arquivos filtrados por ID de equipamento.</li>
                <li><code>curl http://127.0.0.1:5000/files/?equipment_id=1</code></li>
            </ul>
        </li>
        <li><b><code>GET /files/&lt;id&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Obtém metadados de um arquivo pelo ID.</li>
                <li><code>curl http://127.0.0.1:5000/files/1</code></li>
            </ul>
        </li>
        <li><b><code>POST /files/</code></b>
            <ul>
                <li><b>Descrição</b>: Faz o upload de um novo arquivo e salva seus metadados.</li>
                <li><code>curl -X POST -F "file=@/caminho/para/seu/firmware.bin" -F "name=Firmware v1.0" -F "type=firmware" -F "equipment_id=1" -F "uploaded_by=101" http://127.0.0.1:5000/files/</code></li>
            </ul>
        </li>
        <li><b><code>PUT /files/&lt;id&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Atualiza os metadados de um arquivo existente.</li>
                <li><code>curl -X PUT -H "Content-Type: application/json" -d '{"name": "Firmware v1.1 Atualizado", "type": "firmware"}' http://127.0.0.1:5000/files/1</code></li>
            </ul>
        </li>
        <li><b><code>DELETE /files/&lt;id&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Exclui um arquivo (registro e físico).</li>
                <li><code>curl -X DELETE http://127.0.0.1:5000/files/1</code></li>
            </ul>
        </li>
        <li><b><code>GET /files/&lt;id&gt;/download</code></b>
            <ul>
                <li><b>Descrição</b>: Baixa um arquivo.</li>
                <li><code>curl -O -J http://127.0.0.1:5000/files/1/download</code></li>
            </ul>
        </li>
        <li><b><code>POST /files/&lt;id&gt;/download</code></b>
            <ul>
                <li><b>Descrição</b>: Incrementa o contador de downloads de um arquivo.</li>
                <li><code>curl -X POST http://127.0.0.1:5000/files/1/download</code></li>
            </ul>
        </li>
    </ul>

    <h3>Endpoints de Busca (<code>/search</code>)</h3>
    <ul>
        <li><b><code>GET /search/?q=&lt;query&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Realiza busca global em fabricantes e equipamentos.</li>
                <li><code>curl http://127.0.0.1:5000/search/?q=termo</code></li>
            </ul>
        </li>
        <li><b><code>GET /search/manufacturers?q=&lt;query&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Busca fabricantes pelo nome.</li>
                <li><code>curl http://127.0.0.1:5000/search/manufacturers?q=termo</code></li>
            </ul>
        </li>
        <li><b><code>GET /search/equipments?q=&lt;query&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: Busca equipamentos pelo nome ou modelo.</li>
                <li><code>curl http://127.0.0.1:5000/search/equipments?q=termo</code></li>
            </ul>
        </li>
    </ul>

    <h3>Endpoints de Administração (<code>/admin</code>)</h3>
    <ul>
        <li><b><code>GET /admin/stats</code></b>
            <ul>
                <li><b>Descrição</b>: Obtém estatísticas gerais do sistema.</li>
                <li><code>curl http://127.0.0.1:5000/admin/stats</code></li>
            </ul>
        </li>
        <li><b><code>GET /admin/users</code></b>
            <ul>
                <li><b>Descrição</b>: (Placeholder) Lista usuários.</li>
                <li><code>curl http://127.0.0.1:5000/admin/users</code></li>
            </ul>
        </li>
        <li><b><code>PUT /admin/users/&lt;id&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: (Placeholder) Atualiza um usuário.</li>
                <li><code>curl -X PUT -H "Content-Type: application/json" -d '{"username": "novo_usuario"}' http://127.0.0.1:5000/admin/users/1</code></li>
            </ul>
        </li>
        <li><b><code>DELETE /admin/users/&lt;id&gt;</code></b>
            <ul>
                <li><b>Descrição</b>: (Placeholder) Exclui um usuário.</li>
                <li><code>curl -X DELETE http://127.0.0.1:5000/admin/users/1</code></li>
            </ul>
        </li>
    </ul>

    <h2>🤝 Contribuição</h2>
    <p>Sinta-se à vontade para contribuir com melhorias, relatar bugs ou sugerir novas funcionalidades!</p>
    <ol>
        <li>Faça um fork do projeto.</li>
        <li>Crie uma nova branch (<code>git checkout -b feature/minha-nova-feature</code>).</li>
        <li>Faça suas alterações e commit (<code>git commit -m 'feat: Adiciona nova funcionalidade X'</code>).</li>
        <li>Faça push para a branch (<code>git push origin feature/minha-nova-feature</code>).</li>
        <li>Abra um Pull Request.</li>
    </ol>
</body>
</html>
