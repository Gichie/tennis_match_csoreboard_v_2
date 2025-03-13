import logging

from waitress import serve

from src.config.log_config import setup_logger

# Настройка логгирования ДО любых других импортов
setup_logger()

from wsgi import app_with_static

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    logger.info(f"The server is running http://{host}:{port}/")
    serve(app_with_static, host=host, port=port, _quiet=True)
    logger.info(f"The server has stopped")
