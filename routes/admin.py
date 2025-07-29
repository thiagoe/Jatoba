from flask import Blueprint, request, jsonify
from database import get_db_connection, close_db_connection
import logging

admin_bp = Blueprint('admin', __name__)
logger = logging.getLogger('api_jatoba.admin') # Logger específico para admin

# GET /admin/stats - Estatísticas gerais do sistema
@admin_bp.route('/stats', methods=['GET'])
def get_system_stats():
    logger.info("Iniciando obtenção de estatísticas gerais do sistema.")
    conn = get_db_connection()
    if conn is None:
        logger.error("Falha ao obter conexão com o banco de dados para estatísticas.")
        return jsonify({"message": "Erro de conexão ao banco de dados"}), 500
    
    cursor = conn.cursor()
    stats = {}
    try:
        cursor.execute("SELECT COUNT(*) FROM fabricantes")
        stats['total_manufacturers'] = cursor.fetchone()[0]
        logger.debug(f"Total de fabricantes: {stats['total_manufacturers']}.")

        cursor.execute("SELECT COUNT(*) FROM equipamentos")
        stats['total_equipments'] = cursor.fetchone()[0]
        logger.debug(f"Total de equipamentos: {stats['total_equipments']}.")

        cursor.execute("SELECT COUNT(*) FROM arquivos")
        stats['total_files'] = cursor.fetchone()[0]
        logger.debug(f"Total de arquivos: {stats['total_files']}.")

        cursor.execute("SELECT SUM(download_count) FROM arquivos")
        stats['total_downloads'] = cursor.fetchone()[0] or 0
        logger.debug(f"Total de downloads: {stats['total_downloads']}.")

        cursor.execute("SELECT type, COUNT(*) FROM arquivos GROUP BY type")
        stats['files_by_type'] = dict(cursor.fetchall())
        logger.debug(f"Arquivos por tipo: {stats['files_by_type']}.")
        
        logger.info("Estatísticas gerais obtidas com sucesso.")
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}", exc_info=True)
        return jsonify({"message": "Erro ao obter estatísticas", "error": str(e)}), 500
    finally:
        cursor.close()
        close_db_connection(conn)

# Para os endpoints de usuário, estou mantendo os logs como placeholders,
# pois a tabela 'users' não foi definida.
# GET /admin/users - Listar usuários (admin only)
@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    logger.info("Tentativa de listar usuários (funcionalidade 'admin only').")
    # Este é um placeholder. Você precisaria de uma tabela 'users'
    # para implementar isso de fato.
    logger.warning("Endpoint de listagem de usuários não implementado (requer tabela 'users').")
    return jsonify({"message": "Endpoint de listagem de usuários. Implementação da tabela 'users' necessária."}), 501

# PUT /admin/users/:id - Atualizar usuário (admin only)
@admin_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    logger.info(f"Tentativa de atualizar usuário ID {id} (funcionalidade 'admin only').")
    # Este é um placeholder. Você precisaria de uma tabela 'users'
    # para implementar isso de fato.
    logger.warning(f"Endpoint de atualização do usuário {id} não implementado (requer tabela 'users').")
    return jsonify({"message": f"Endpoint de atualização do usuário {id}. Implementação da tabela 'users' necessária."}), 501

# DELETE /admin/users/:id - Excluir usuário (admin only)
@admin_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    logger.info(f"Tentativa de excluir usuário ID {id} (funcionalidade 'admin only').")
    # Este é um placeholder. Você precisaria de uma tabela 'users'
    # para implementar isso de fato.
    logger.warning(f"Endpoint de exclusão do usuário {id} não implementado (requer tabela 'users').")
    return jsonify({"message": f"Endpoint de exclusão do usuário {id}. Implementação da tabela 'users' necessária."}), 501
