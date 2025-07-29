import os
from flask import Blueprint, request, jsonify, current_app
from database import get_db_connection, close_db_connection
from werkzeug.utils import secure_filename
import logging

equipments_bp = Blueprint('equipments', __name__)
logger = logging.getLogger('api_jatoba.equipments') # Logger específico para equipamentos

# GET /equipments - Listar todos os equipamentos
# GET /equipments?manufacturer_id=:id - Listar equipamentos por fabricante
@equipments_bp.route('/', methods=['GET'])
def get_all_equipments():
    manufacturer_id = request.args.get('manufacturer_id')
    logger.info(f"Iniciando listagem de equipamentos. Filtro por fabricante_id: {manufacturer_id if manufacturer_id else 'Nenhum'}.")
    
    conn = get_db_connection()
    if conn is None:
        logger.error("Falha ao obter conexão com o banco de dados para listar equipamentos.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    
    try:
        if manufacturer_id:
            cursor.execute(
                "SELECT id, name, model, manufacturer_id, image_url, created_at, updated_at FROM equipamentos WHERE manufacturer_id = %s",
                (manufacturer_id,)
            )
        else:
            cursor.execute("SELECT id, name, model, manufacturer_id, image_url, created_at, updated_at FROM equipamentos")
        
        equipments = cursor.fetchall()
        logger.info(f"Listados {len(equipments)} equipamentos.")
        return jsonify(equipments), 200
    except Exception as e:
        logger.error(f"Erro ao listar equipamentos: {e}", exc_info=True)
        return jsonify({"message": "Erro ao listar equipamentos", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# GET /equipments/:id - Obter equipamento específico
@equipments_bp.route('/<int:id>', methods=['GET'])
def get_equipment_by_id(id):
    logger.info(f"Buscando equipamento com ID: {id}.")
    conn = get_db_connection()
    if conn is None:
        logger.error(f"Falha ao obter conexão com o banco de dados para buscar equipamento {id}.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, model, manufacturer_id, image_url, created_at, updated_at FROM equipamentos WHERE id = %s", (id,))
        equipment = cursor.fetchone()
        if equipment:
            logger.info(f"Equipamento ID {id} encontrado: {equipment['name']}.")
            return jsonify(equipment), 200
        logger.warning(f"Equipamento ID {id} não encontrado.")
        return jsonify({"message": "Equipamento não encontrado"}), 404
    except Exception as e:
        logger.error(f"Erro ao obter equipamento ID {id}: {e}", exc_info=True)
        return jsonify({"message": "Erro ao obter equipamento", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# POST /equipments - Criar novo equipamento
@equipments_bp.route('/', methods=['POST'])
def create_equipment():
    data = request.json
    name = data.get('name')
    model = data.get('model')
    manufacturer_id = data.get('manufacturer_id')
    image_url = data.get('image_url')

    if not all([name, model]):
        logger.warning("Tentativa de criar equipamento sem nome ou modelo.")
        return jsonify({"message": "Nome e modelo do equipamento são obrigatórios"}), 400

    logger.info(f"Tentando criar novo equipamento: {name} ({model}).")
    conn = get_db_connection()
    if conn is None:
        logger.error("Falha ao obter conexão com o banco de dados para criar equipamento.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO equipamentos (name, model, manufacturer_id, image_url) VALUES (%s, %s, %s, %s)",
            (name, model, manufacturer_id, image_url)
        )
        conn.commit()
        new_id = cursor.lastrowid
        logger.info(f"Equipamento '{name} ({model})' criado com sucesso, ID: {new_id}.")
        return jsonify({"message": "Equipamento criado com sucesso", "id": new_id}), 201
    except Exception as e:
        logger.error(f"Erro ao criar equipamento '{name} ({model})': {e}", exc_info=True)
        return jsonify({"message": "Erro ao criar equipamento", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# PUT /equipments/:id - Atualizar equipamento
@equipments_bp.route('/<int:id>', methods=['PUT'])
def update_equipment(id):
    data = request.json
    name = data.get('name')
    model = data.get('model')
    manufacturer_id = data.get('manufacturer_id')
    image_url = data.get('image_url')

    logger.info(f"Tentando atualizar equipamento ID: {id}.")
    conn = get_db_connection()
    if conn is None:
        logger.error(f"Falha ao obter conexão com o banco de dados para atualizar equipamento {id}.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE equipamentos SET name = %s, model = %s, manufacturer_id = %s, image_url = %s WHERE id = %s",
            (name, model, manufacturer_id, image_url, id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            logger.warning(f"Equipamento ID {id} não encontrado para atualização.")
            return jsonify({"message": "Equipamento não encontrado para atualização"}), 404
        logger.info(f"Equipamento ID {id} atualizado com sucesso.")
        return jsonify({"message": "Equipamento atualizado com sucesso"}), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar equipamento ID {id}: {e}", exc_info=True)
        return jsonify({"message": "Erro ao atualizar equipamento", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# DELETE /equipments/:id - Excluir equipamento
@equipments_bp.route('/<int:id>', methods=['DELETE'])
def delete_equipment(id):
    logger.info(f"Tentando excluir equipamento ID: {id}.")
    conn = get_db_connection()
    if conn is None:
        logger.error(f"Falha ao obter conexão com o banco de dados para excluir equipamento {id}.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM equipamentos WHERE id = %s", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            logger.warning(f"Equipamento ID {id} não encontrado para exclusão.")
            return jsonify({"message": "Equipamento não encontrado para exclusão"}), 404
        logger.info(f"Equipamento ID {id} excluído com sucesso.")
        return jsonify({"message": "Equipamento excluído com sucesso"}), 200
    except Exception as e:
        logger.error(f"Erro ao excluir equipamento ID {id}: {e}", exc_info=True)
        return jsonify({"message": "Erro ao excluir equipamento", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# POST /equipments/:id/image - Upload da imagem do equipamento
@equipments_bp.route('/<int:id>/image', methods=['POST'])
def upload_equipment_image(id):
    logger.info(f"Iniciando upload de imagem para equipamento ID: {id}.")
    if 'image' not in request.files:
        logger.warning(f"Upload de imagem para equipamento {id}: Nenhuma imagem na requisição.")
        return jsonify({"message": "Nenhuma imagem na requisição"}), 400
    
    image = request.files['image']
    if image.filename == '':
        logger.warning(f"Upload de imagem para equipamento {id}: Nenhuma imagem selecionada.")
        return jsonify({"message": "Nenhuma imagem selecionada"}), 400
    
    if image:
        original_filename = image.filename
        filename = secure_filename(f"equipment_image_{id}_{original_filename}")
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        try:
            image.save(file_path)
            logger.info(f"Imagem '{original_filename}' salva para equipamento {id} em: {file_path}")
        except Exception as e:
            logger.error(f"Erro ao salvar o arquivo de imagem para equipamento {id}: {str(e)}", exc_info=True)
            return jsonify({"message": f"Erro ao salvar o arquivo: {str(e)}"}), 500
        
        conn = get_db_connection()
        if conn is None:
            logger.error(f"Falha ao obter conexão com o banco de dados para atualizar imagem do equipamento {id}.")
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.warning(f"Arquivo de imagem '{filename}' removido após falha na conexão com DB.")
            return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
        
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE equipamentos SET image_url = %s WHERE id = %s",
                (file_path, id)
            )
            conn.commit()
            if cursor.rowcount == 0:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.warning(f"Equipamento ID {id} não encontrado para associar imagem. Arquivo '{filename}' removido.")
                return jsonify({"message": "Equipamento não encontrado para associar a imagem"}), 404
            
            logger.info(f"URL da imagem para equipamento {id} atualizada no banco de dados para: {file_path}.")
            return jsonify({"message": "Imagem do equipamento uploaded e atualizada com sucesso", "image_url": file_path}), 200
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.error(f"Erro ao atualizar URL da imagem para equipamento {id} no DB: {str(e)}. Arquivo '{filename}' removido.", exc_info=True)
            return jsonify({"message": "Erro ao atualizar URL da imagem no banco de dados", "error": str(e)}), 500
        finally:
            cursor.close()
            close_db_connection(conn)
    
    logger.error(f"Erro desconhecido no upload da imagem para equipamento ID: {id}.")
    return jsonify({"message": "Erro desconhecido no upload da imagem"}), 500