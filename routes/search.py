from flask import Blueprint, request, jsonify
from database import get_db_connection, close_db_connection
import logging

search_bp = Blueprint('search', __name__)
logger = logging.getLogger('api_jatoba.search') # Logger específico para busca

# GET /search?q=:query - Busca global em equipamentos e fabricantes
@search_bp.route('/', methods=['GET'])
def global_search():
    query = request.args.get('q')
    logger.info(f"Iniciando busca global com query: '{query}'.")
    if not query:
        logger.warning("Busca global: Parâmetro 'q' ausente.")
        return jsonify({"message": "Parâmetro de busca 'q' é obrigatório"}), 400

    conn = get_db_connection()
    if conn is None:
        logger.error("Falha ao obter conexão com o banco de dados para busca global.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    results = {}
    
    try:
        # Busca em fabricantes
        cursor.execute(
            "SELECT id, name, logo_url FROM fabricantes WHERE name LIKE %s",
            (f"%{query}%",)
        )
        manufacturers_found = cursor.fetchall()
        results['manufacturers'] = manufacturers_found
        logger.info(f"Busca global: Encontrados {len(manufacturers_found)} fabricantes para '{query}'.")

        # Busca em equipamentos
        cursor.execute(
            "SELECT id, name, model, manufacturer_id, image_url FROM equipamentos WHERE name LIKE %s OR model LIKE %s",
            (f"%{query}%", f"%{query}%")
        )
        equipments_found = cursor.fetchall()
        results['equipments'] = equipments_found
        logger.info(f"Busca global: Encontrados {len(equipments_found)} equipamentos para '{query}'.")

        return jsonify(results), 200
    except Exception as e:
        logger.error(f"Erro na busca global para '{query}': {e}", exc_info=True)
        return jsonify({"message": "Erro na busca global", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# GET /search/manufacturers?q=:query - Busca específica em fabricantes
@search_bp.route('/manufacturers', methods=['GET'])
def search_manufacturers():
    query = request.args.get('q')
    logger.info(f"Iniciando busca em fabricantes com query: '{query}'.")
    if not query:
        logger.warning("Busca em fabricantes: Parâmetro 'q' ausente.")
        return jsonify({"message": "Parâmetro de busca 'q' é obrigatório"}), 400

    conn = get_db_connection()
    if conn is None:
        logger.error("Falha ao obter conexão com o banco de dados para busca de fabricantes.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, name, logo_url FROM fabricantes WHERE name LIKE %s",
            (f"%{query}%",)
        )
        manufacturers = cursor.fetchall()
        logger.info(f"Busca em fabricantes: Encontrados {len(manufacturers)} resultados para '{query}'.")
        return jsonify(manufacturers), 200
    except Exception as e:
        logger.error(f"Erro na busca de fabricantes para '{query}': {e}", exc_info=True)
        return jsonify({"message": "Erro na busca de fabricantes", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# GET /search/equipments?q=:query - Busca específica em equipamentos
@search_bp.route('/equipments', methods=['GET'])
def search_equipments():
    query = request.args.get('q')
    logger.info(f"Iniciando busca em equipamentos com query: '{query}'.")
    if not query:
        logger.warning("Busca em equipamentos: Parâmetro 'q' ausente.")
        return jsonify({"message": "Parâmetro de busca 'q' é obrigatório"}), 400

    conn = get_db_connection()
    if conn is None:
        logger.error("Falha ao obter conexão com o banco de dados para busca de equipamentos.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, name, model, manufacturer_id, image_url FROM equipamentos WHERE name LIKE %s OR model LIKE %s",
            (f"%{query}%", f"%{query}%")
        )
        equipments = cursor.fetchall()
        logger.info(f"Busca em equipamentos: Encontrados {len(equipments)} resultados para '{query}'.")
        return jsonify(equipments), 200
    except Exception as e:
        logger.error(f"Erro na busca de equipamentos para '{query}': {e}", exc_info=True)
        return jsonify({"message": "Erro na busca de equipamentos", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)