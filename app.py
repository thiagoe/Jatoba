import os
from flask import Flask, jsonify, request
from config import Config
from logger import app_logger # Importa o logger

# Certifica-se de que a pasta de uploads existe
if not os.path.exists(Config.UPLOAD_FOLDER):
    os.makedirs(Config.UPLOAD_FOLDER)

app = Flask(__name__)
app.config.from_object(Config)

# Registrar o logger na aplicação para ser acessível via current_app.logger (opcional, mas boa prática)
app.logger.handlers = app_logger.handlers
app.logger.setLevel(app_logger.level)

# Importar e registrar os Blueprints
from routes.manufacturers import manufacturers_bp
from routes.equipments import equipments_bp
from routes.files import files_bp
from routes.search import search_bp
from routes.admin import admin_bp

app.register_blueprint(manufacturers_bp, url_prefix='/manufacturers')
app.register_blueprint(equipments_bp, url_prefix='/equipments')
app.register_blueprint(files_bp, url_prefix='/files')
app.register_blueprint(search_bp, url_prefix='/search')
app.register_blueprint(admin_bp, url_prefix='/admin')

# Exemplo de logging para requisições
@app.before_request
def log_request_info():
    app.logger.info(f"Requisição recebida: {request.method} {request.url} de {request.remote_addr}")

@app.after_request
def log_response_info(response):
    app.logger.info(f"Requisição finalizada: {request.method} {request.url} com status {response.status_code}")
    return response

# Endpoint genérico de upload (fora dos blueprints específicos de entidade)
@app.route('/upload', methods=['POST'])
def generic_upload():
    app_logger.info("Requisição de upload genérico iniciada.")
    if 'file' not in request.files:
        app_logger.warning("Upload genérico: Nenhum arquivo na requisição.")
        return jsonify({"message": "Nenhum arquivo na requisição"}), 400
    
    file = request.files['file']
    if file.filename == '':
        app_logger.warning("Upload genérico: Nenhum arquivo selecionado.")
        return jsonify({"message": "Nenhum arquivo selecionado"}), 400
    
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(file_path)
            app_logger.info(f"Upload genérico de '{filename}' bem-sucedido. Salvo em: {file_path}")
            return jsonify({"message": "Upload genérico bem-sucedido", "file_url": file_path}), 201
        except Exception as e:
            app_logger.error(f"Erro ao salvar arquivo em upload genérico: {e}", exc_info=True)
            return jsonify({"message": "Erro no upload genérico"}), 500
    
    app_logger.error("Erro desconhecido no upload genérico.")
    return jsonify({"message": "Erro desconhecido no upload genérico"}), 500

@app.route('/upload/<filename>', methods=['DELETE'])
def delete_uploaded_file(filename):
    app_logger.info(f"Requisição de exclusão de arquivo genérico iniciada para: {filename}")
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            app_logger.info(f"Arquivo genérico '{filename}' deletado com sucesso do sistema de arquivos.")
            return jsonify({"message": f"Arquivo '{filename}' deletado com sucesso."}), 200
        except OSError as e:
            app_logger.error(f"Erro ao deletar arquivo genérico '{filename}': {e}", exc_info=True)
            return jsonify({"message": f"Erro ao deletar arquivo: {e}"}), 500
    app_logger.warning(f"Tentativa de deletar arquivo genérico não encontrado: {filename}.")
    return jsonify({"message": "Arquivo não encontrado."}), 404


@app.route('/')
def home():
    app_logger.info("Acessada rota raiz.")
    return "API Jatoba em execução!"

if __name__ == '__main__':
    app.run(debug=True)