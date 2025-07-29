import os
from flask import Blueprint, request, jsonify, current_app
from database import get_db_connection, close_db_connection
from werkzeug.utils import secure_filename
import logging # Importa o módulo logging

manufacturers_bp = Blueprint('manufacturers', __name__)
# Obtém o logger para este blueprint (o nome pode ser o nome do blueprint ou algo mais específico)
logger = logging.getLogger('api_jatoba.manufacturers')


# GET /manufacturers - Listar todos os fabricantes
@manufacturers_bp.route('/', methods=['GET'])
def get_all_manufacturers():
    logger.info("Iniciando listagem de todos os fabricantes.")
    conn = get_db_connection()
    if conn is None:
        logger.error("Falha ao obter conexão com o banco de dados para listar fabricantes.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, logo_url, created_at, updated_at FROM fabricantes")
        manufacturers = cursor.fetchall()
        logger.info(f"Listados {len(manufacturers)} fabricantes.")
        return jsonify(manufacturers), 200
    except Exception as e:
        logger.error(f"Erro ao listar fabricantes: {e}", exc_info=True) # exc_info=True para incluir stack trace
        return jsonify({"message": "Erro ao listar fabricantes", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# GET /manufacturers/:id - Obter fabricante específico
@manufacturers_bp.route('/<int:id>', methods=['GET'])
def get_manufacturer_by_id(id):
    logger.info(f"Buscando fabricante com ID: {id}.")
    conn = get_db_connection()
    if conn is None:
        logger.error(f"Falha ao obter conexão com o banco de dados para buscar fabricante {id}.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, logo_url, created_at, updated_at FROM fabricantes WHERE id = %s", (id,))
        manufacturer = cursor.fetchone()
        if manufacturer:
            logger.info(f"Fabricante ID {id} encontrado: {manufacturer['name']}.")
            return jsonify(manufacturer), 200
        logger.warning(f"Fabricante ID {id} não encontrado.")
        return jsonify({"message": "Fabricante não encontrado"}), 404
    except Exception as e:
        logger.error(f"Erro ao obter fabricante ID {id}: {e}", exc_info=True)
        return jsonify({"message": "Erro ao obter fabricante", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# POST /manufacturers - Criar novo fabricante
@manufacturers_bp.route('/', methods=['POST'])
def create_manufacturer():
    data = request.json
    name = data.get('name')
    logo_url = data.get('logo_url')

    if not name:
        logger.warning("Tentativa de criar fabricante sem nome.")
        return jsonify({"message": "Nome do fabricante é obrigatório"}), 400

    logger.info(f"Tentando criar novo fabricante: {name}.")
    conn = get_db_connection()
    if conn is None:
        logger.error("Falha ao obter conexão com o banco de dados para criar fabricante.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO fabricantes (name, logo_url) VALUES (%s, %s)",
            (name, logo_url)
        )
        conn.commit()
        new_id = cursor.lastrowid
        logger.info(f"Fabricante '{name}' criado com sucesso, ID: {new_id}.")
        return jsonify({"message": "Fabricante criado com sucesso", "id": new_id}), 201
    except Exception as e:
        logger.error(f"Erro ao criar fabricante '{name}': {e}", exc_info=True)
        return jsonify({"message": "Erro ao criar fabricante", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# PUT /manufacturers/:id - Atualizar fabricante
@manufacturers_bp.route('/<int:id>', methods=['PUT'])
def update_manufacturer(id):
    data = request.json
    name = data.get('name')
    logo_url = data.get('logo_url')

    logger.info(f"Tentando atualizar fabricante ID: {id}.")
    conn = get_db_connection()
    if conn is None:
        logger.error(f"Falha ao obter conexão com o banco de dados para atualizar fabricante {id}.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE fabricantes SET name = %s, logo_url = %s WHERE id = %s",
            (name, logo_url, id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            logger.warning(f"Fabricante ID {id} não encontrado para atualização.")
            return jsonify({"message": "Fabricante não encontrado para atualização"}), 404
        logger.info(f"Fabricante ID {id} atualizado com sucesso.")
        return jsonify({"message": "Fabricante atualizado com sucesso"}), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar fabricante ID {id}: {e}", exc_info=True)
        return jsonify({"message": "Erro ao atualizar fabricante", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# DELETE /manufacturers/:id - Excluir fabricante
@manufacturers_bp.route('/<int:id>', methods=['DELETE'])
def delete_manufacturer(id):
    logger.info(f"Tentando excluir fabricante ID: {id}.")
    conn = get_db_connection()
    if conn is None:
        logger.error(f"Falha ao obter conexão com o banco de dados para excluir fabricante {id}.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM fabricantes WHERE id = %s", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            logger.warning(f"Fabricante ID {id} não encontrado para exclusão.")
            return jsonify({"message": "Fabricante não encontrado para exclusão"}), 404
        logger.info(f"Fabricante ID {id} excluído com sucesso.")
        return jsonify({"message": "Fabricante excluído com sucesso"}), 200
    except Exception as e:
        logger.error(f"Erro ao excluir fabricante ID {id}: {e}", exc_info=True)
        return jsonify({"message": "Erro ao excluir fabricante", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# POST /manufacturers/:id/logo - Upload do logo do fabricante
@manufacturers_bp.route('/<int:id>/logo', methods=['POST'])
def upload_manufacturer_logo(id):
    logger.info(f"Iniciando upload de logo para fabricante ID: {id}.")
    if 'logo' not in request.files:
        logger.warning(f"Upload de logo para fabricante {id}: Nenhum arquivo na requisição.")
        return jsonify({"message": "Nenhum arquivo de logo na requisição"}), 400
    
    logo = request.files['logo']
    if logo.filename == '':
        logger.warning(f"Upload de logo para fabricante {id}: Nenhum arquivo selecionado.")
        return jsonify({"message": "Nenhum arquivo de logo selecionado"}), 400
    
    if logo:
        original_filename = logo.filename
        filename = secure_filename(f"manufacturer_logo_{id}_{original_filename}")
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        try:
            logo.save(file_path)
            logger.info(f"Logo '{original_filename}' salvo para fabricante {id} em: {file_path}")
        except Exception as e:
            logger.error(f"Erro ao salvar o arquivo de logo para fabricante {id}: {str(e)}", exc_info=True)
            return jsonify({"message": f"Erro ao salvar o arquivo: {str(e)}"}), 500
        
        conn = get_db_connection()
        if conn is None:
            logger.error(f"Falha ao obter conexão com o banco de dados para atualizar logo do fabricante {id}.")
            # Tenta remover o arquivo salvo se a conexão com o DB falhar
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.warning(f"Arquivo de logo '{filename}' removido após falha na conexão com DB.")
            return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
        
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE fabricantes SET logo_url = %s WHERE id = %s",
                (file_path, id)
            )
            conn.commit()
            if cursor.rowcount == 0:
                # Se o fabricante não foi encontrado, exclua o logo recém-carregado
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.warning(f"Fabricante ID {id} não encontrado para associar logo. Arquivo '{filename}' removido.")
                return jsonify({"message": "Fabricante não encontrado para associar o logo"}), 404
            
            logger.info(f"URL do logo para fabricante {id} atualizada no banco de dados para: {file_path}.")
            return jsonify({"message": "Logo do fabricante uploaded e atualizado com sucesso", "logo_url": file_path}), 200
        except Exception as e:
            # Em caso de erro no DB, remova o arquivo que foi salvo
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.error(f"Erro ao atualizar URL do logo para fabricante {id} no DB: {str(e)}. Arquivo '{filename}' removido.", exc_info=True)
            return jsonify({"message": "Erro ao atualizar URL do logo no banco de dados", "error": str(e)}), 500
        finally:
            cursor.close()
            close_db_connection(conn)
    
    logger.error(f"Erro desconhecido no upload do logo para fabricante ID: {id}.")
    return jsonify({"message": "Erro desconhecido no upload do logo"}), 500