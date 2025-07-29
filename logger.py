import logging
import os
from config import Config

def setup_logging():
    # Cria o diretório para o log se não existir (se LOG_FILE incluir subdiretórios)
    log_dir = os.path.dirname(Config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configura o logger raiz
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL), # Define o nível do log (INFO, DEBUG, ERROR, etc.)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # Formato da mensagem
        handlers=[
            logging.FileHandler(Config.LOG_FILE, encoding='utf-8'), # Salva logs em arquivo
            logging.StreamHandler() # Exibe logs no console
        ]
    )
    # Define o nível do logger do PyMySQL para evitar logs excessivos de debug da biblioteca
    logging.getLogger('pymysql').setLevel(logging.WARNING)
    logging.getLogger('werkzeug').setLevel(logging.WARNING) # Evita logs excessivos do servidor Flask

    return logging.getLogger('api_jatoba') # Retorna um logger específico para nossa API

# Inicializa o logger para a aplicação
app_logger = setup_logging()