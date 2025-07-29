import os
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from database import get_db_connection, close_db_connection
from werkzeug.utils import secure_filename
import logging

files_bp = Blueprint('files', __name__)
logger = logging.getLogger('api_jatoba.files') # Logger específico para arquivos

# GET /files - Listar todos os arquivos
# GET /files?equipment_id=:id - Listar arquivos por equipamento
# GET /files?type=firmware - Listar apenas firmwares
# GET /files?type=document - Listar apenas documentos
@files_bp.route('/', methods=['GET'])
def get_all_files():
    equipment_id = request.args.get('equipment_id')
    file_type = request.args.get('type') # 'firmware' ou 'document'
    
    logger.info(f"Iniciando listagem de arquivos. Filtros: equipment_id={equipment_id}, type={file_type}.")

    conn = get_db_connection()
    if conn is None:
        logger.error("Falha ao obter conexão com o banco de dados para listar arquivos.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    sql_query = "SELECT id, name, type, equipment_id, file_url, file_size, download_count, uploaded_by, created_at, updated_at FROM arquivos"
    params = []
    conditions = []

    if equipment_id:
        conditions.append("equipment_id = %s")
        params.append(equipment_id)
    
    if file_type:
        if file_type not in ['firmware', 'document']:
            logger.warning(f"Tentativa de listar arquivos com tipo inválido: '{file_type}'.")
            return jsonify({"message": "Tipo de arquivo inválido. Use 'firmware' ou 'document'."}), 400
        conditions.append("type = %s")
        params.append(file_type)
    
    if conditions:
        sql_query += " WHERE " + " AND ".join(conditions)
    
    try:
        cursor.execute(sql_query, tuple(params))
        files = cursor.fetchall()
        logger.info(f"Listados {len(files)} arquivos com os filtros aplicados.")
        return jsonify(files), 200
    except Exception as e:
        logger.error(f"Erro ao listar arquivos: {e}", exc_info=True)
        return jsonify({"message": "Erro ao listar arquivos", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# GET /files/:id - Obter arquivo específico
@files_bp.route('/<int:id>', methods=['GET'])
def get_file_by_id(id):
    logger.info(f"Buscando arquivo com ID: {id}.")
    conn = get_db_connection()
    if conn is None:
        logger.error(f"Falha ao obter conexão com o banco de dados para buscar arquivo {id}.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, type, equipment_id, file_url, file_size, download_count, uploaded_by, created_at, updated_at FROM arquivos WHERE id = %s", (id,))
        file_data = cursor.fetchone()
        if file_data:
            logger.info(f"Arquivo ID {id} encontrado: {file_data['name']}.")
            return jsonify(file_data), 200
        logger.warning(f"Arquivo ID {id} não encontrado.")
        return jsonify({"message": "Arquivo não encontrado"}), 404
    except Exception as e:
        logger.error(f"Erro ao obter arquivo ID {id}: {e}", exc_info=True)
        return jsonify({"message": "Erro ao obter arquivo", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# POST /files - Upload de novo arquivo
@files_bp.route('/', methods=['POST'])
def upload_new_file():
    logger.info("Iniciando upload de novo arquivo.")
    if 'file' not in request.files:
        logger.warning("Upload de arquivo: Nenhum arquivo na requisição.")
        return jsonify({"message": "Nenhum arquivo na requisição"}), 400
    
    file = request.files['file']
    if file.filename == '':
        logger.warning("Upload de arquivo: Nenhum arquivo selecionado.")
        return jsonify({"message": "Nenhum arquivo selecionado"}), 400
    
    name = request.form.get('name') or secure_filename(file.filename)
    file_type = request.form.get('type')
    equipment_id = request.form.get('equipment_id', type=int)
    uploaded_by = request.form.get('uploaded_by', type=int)
    
    if not file_type or file_type not in ['firmware', 'document']:
        logger.warning(f"Upload de arquivo: Tipo inválido ou ausente: '{file_type}'.")
        return jsonify({"message": "Tipo de arquivo inválido ou ausente. Use 'firmware' ou 'document'."}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path_on_server = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(file_path_on_server)
            file_size = os.path.getsize(file_path_on_server)
            logger.info(f"Arquivo '{original_filename}' salvo em: {file_path_on_server}")
        except Exception as e:
            logger.error(f"Erro ao salvar o arquivo físico: {str(e)}", exc_info=True)
            return jsonify({"message": f"Erro ao salvar o arquivo: {str(e)}"}), 500
        
        conn = get_db_connection()
        if conn is None:
            logger.error("Falha ao obter conexão com o banco de dados para salvar metadados do arquivo.")
            if os.path.exists(file_path_on_server):
                os.remove(file_path_on_server)
                logger.warning(f"Arquivo '{filename}' removido após falha na conexão com DB.")
            return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
        
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO arquivos (name, type, equipment_id, file_url, file_size, uploaded_by) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, file_type, equipment_id, file_path_on_server, file_size, uploaded_by)
            )
            conn.commit()
            logger.info(f"Metadados do arquivo '{name}' salvos com sucesso, ID: {cursor.lastrowid}.")
            return jsonify({"message": "Arquivo uploaded e metadados salvos com sucesso", "id": cursor.lastrowid, "file_url": file_path_on_server}), 201
        except Exception as e:
            if os.path.exists(file_path_on_server):
                os.remove(file_path_on_server)
                logger.error(f"Erro ao salvar metadados do arquivo no banco de dados: {str(e)}. Arquivo '{filename}' removido.", exc_info=True)
            return jsonify({"message": "Erro ao salvar metadados do arquivo no banco de dados", "error": str(e)}), 500
        finally:
            cursor.close()
            close_db_connection(conn)
    
    logger.error("Erro desconhecido no upload do arquivo.")
    return jsonify({"message": "Erro desconhecido no upload do arquivo"}), 500


# PUT /files/:id - Atualizar metadados do arquivo
@files_bp.route('/<int:id>', methods=['PUT'])
def update_file_metadata(id):
    data = request.json
    name = data.get('name')
    file_type = data.get('type')
    equipment_id = data.get('equipment_id')
    uploaded_by = data.get('uploaded_by')

    logger.info(f"Tentando atualizar metadados do arquivo ID: {id}.")
    if file_type and file_type not in ['firmware', 'document']:
        logger.warning(f"Atualização de metadados para arquivo {id}: Tipo inválido: '{file_type}'.")
        return jsonify({"message": "Tipo de arquivo inválido. Use 'firmware' ou 'document'."}), 400

    conn = get_db_connection()
    if conn is None:
        logger.error(f"Falha ao obter conexão com o banco de dados para atualizar metadados do arquivo {id}.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        set_clauses = []
        params = []
        if name is not None:
            set_clauses.append("name = %s")
            params.append(name)
        if file_type is not None:
            set_clauses.append("type = %s")
            params.append(file_type)
        if equipment_id is not None:
            set_clauses.append("equipment_id = %s")
            params.append(equipment_id)
        if uploaded_by is not None:
            set_clauses.append("uploaded_by = %s")
            params.append(uploaded_by)
        
        if not set_clauses:
            logger.warning(f"Atualização de metadados para arquivo {id}: Nenhum dado fornecido.")
            return jsonify({"message": "Nenhum dado fornecido para atualização"}), 400
        
        sql_query = "UPDATE arquivos SET " + ", ".join(set_clauses) + " WHERE id = %s"
        params.append(id)

        cursor.execute(sql_query, tuple(params))
        conn.commit()
        if cursor.rowcount == 0:
            logger.warning(f"Arquivo ID {id} não encontrado para atualização de metadados.")
            return jsonify({"message": "Arquivo não encontrado para atualização"}), 404
        logger.info(f"Metadados do arquivo ID {id} atualizados com sucesso.")
        return jsonify({"message": "Metadados do arquivo atualizados com sucesso"}), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar metadados do arquivo ID {id}: {e}", exc_info=True)
        return jsonify({"message": "Erro ao atualizar metadados do arquivo", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# DELETE /files/:id - Excluir arquivo
@files_bp.route('/<int:id>', methods=['DELETE'])
def delete_file(id):
    logger.info(f"Tentando excluir arquivo ID: {id}.")
    conn = get_db_connection()
    if conn is None:
        logger.error(f"Falha ao obter conexão com o banco de dados para excluir arquivo {id}.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    file_path = None
    try:
        cursor.execute("SELECT file_url FROM arquivos WHERE id = %s", (id,))
        file_data = cursor.fetchone()
        
        if not file_data:
            logger.warning(f"Arquivo ID {id} não encontrado para exclusão.")
            return jsonify({"message": "Arquivo não encontrado para exclusão"}), 404
        
        file_path = file_data['file_url']
        
        cursor.execute("DELETE FROM arquivos WHERE id = %s", (id,))
        conn.commit()
        logger.info(f"Registro do arquivo ID {id} excluído do banco de dados.")

        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Arquivo físico '{file_path}' deletado do sistema de arquivos.")
            except OSError as e:
                logger.error(f"Aviso: Não foi possível deletar o arquivo físico {file_path} para o registro {id}: {e}", exc_info=True)
        else:
            logger.warning(f"Arquivo físico associado ao ID {id} não encontrado no sistema de arquivos: {file_path}.")
        
        return jsonify({"message": "Arquivo excluído com sucesso"}), 200
    except Exception as e:
        logger.error(f"Erro ao excluir arquivo ID {id}: {e}", exc_info=True)
        return jsonify({"message": "Erro ao excluir arquivo", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# GET /files/:id/download - Download do arquivo
@files_bp.route('/<int:id>/download', methods=['GET'])
def download_file(id):
    logger.info(f"Iniciando download para arquivo ID: {id}.")
    conn = get_db_connection()
    if conn is None:
        logger.error(f"Falha ao obter conexão com o banco de dados para download do arquivo {id}.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name, file_url FROM arquivos WHERE id = %s", (id,))
        file_data = cursor.fetchone()
        
        if not file_data:
            logger.warning(f"Arquivo ID {id} não encontrado para download.")
            return jsonify({"message": "Arquivo não encontrado"}), 404
        
        filename = file_data['name']
        file_path = file_data['file_url']
        
        directory = os.path.dirname(file_path)
        file_basename = os.path.basename(file_path)

        if not os.path.exists(file_path):
             logger.warning(f"Arquivo físico '{file_path}' para ID {id} não encontrado no servidor.")
             return jsonify({"message": "Arquivo físico não encontrado no servidor"}), 404

        logger.info(f"Preparando download do arquivo '{filename}' (ID: {id}) de {file_path}.")
        return send_from_directory(directory, file_basename, as_attachment=True, download_name=filename)
    except Exception as e:
        logger.error(f"Erro ao preparar download do arquivo ID {id}: {e}", exc_info=True)
        return jsonify({"message": "Erro ao preparar download do arquivo", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# POST /files/:id/download - Incrementar contador de downloads
@files_bp.route('/<int:id>/download', methods=['POST'])
def increment_download_count(id):
    logger.info(f"Incrementando contador de downloads para arquivo ID: {id}.")
    conn = get_db_connection()
    if conn is None:
        logger.error(f"Falha ao obter conexão com o banco de dados para incrementar download do arquivo {id}.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE arquivos SET download_count = download_count + 1 WHERE id = %s",
            (id,)
        )
        conn.commit()
        if cursor.rowcount == 0:
            logger.warning(f"Arquivo ID {id} não encontrado para incrementar download.")
            return jsonify({"message": "Arquivo não encontrado para incrementar download"}), 404
        
        cursor.execute("SELECT download_count FROM arquivos WHERE id = %s", (id,))
        new_count = cursor.fetchone()
        
        logger.info(f"Contador de downloads para arquivo ID {id} incrementado para: {new_count[0] if new_count else 'N/A'}.")
        return jsonify({"message": "Contador de downloads incrementado", "new_download_count": new_count[0] if new_count else None}), 200
    except Exception as e:
        logger.error(f"Erro ao incrementar contador de downloads para arquivo ID {id}: {e}", exc_info=True)
        return jsonify({"message": "Erro ao incrementar contador de downloads", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)