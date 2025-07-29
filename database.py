import pymysql
from pymysql import Error
from config import Config
import logging # Importa o módulo logging

# O logger já foi configurado em logger.py, apenas o obtemos aqui
db_logger = logging.getLogger('api_jatoba.database')

def get_db_connection():
    """Cria e retorna uma nova conexão com o banco de dados usando PyMySQL."""
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        db_logger.info("Conexão ao banco de dados estabelecida com sucesso.")
        return conn
    except Error as e:
        db_logger.error(f"Erro ao conectar ao MariaDB com PyMySQL: {e}", exc_info=True)
        return None

def close_db_connection(conn):
    """Fecha a conexão com o banco de dados, se estiver aberta."""
    if conn and conn.open:
        try:
            conn.close()
            db_logger.info("Conexão ao banco de dados fechada com sucesso.")
        except Error as e:
            db_logger.error(f"Erro ao fechar conexão com o banco de dados: {e}", exc_info=True)

# Exemplo de uso
if __name__ == '__main__':
    conn = get_db_connection()
    if conn:
        print("Conexão bem-sucedida ao banco de dados com PyMySQL!")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"Resultado de SELECT 1: {result}")
            db_logger.info("Query de teste 'SELECT 1' executada com sucesso.")
        except Error as e:
            print(f"Erro ao executar query: {e}")
            db_logger.error(f"Erro ao executar query de teste: {e}", exc_info=True)
        finally:
            cursor.close()
            close_db_connection(conn)