import os
from dotenv import load_dotenv

load_dotenv() # Carrega as variáveis do .env

class Config:
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    UPLOAD_FOLDER = os.path.abspath(os.getenv('UPLOAD_FOLDER', './uploads'))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limite de 16MB para uploads

    # Configurações de Logging
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.log')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper() # Nível padrão: INFO