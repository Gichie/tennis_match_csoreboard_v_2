from waitress import serve

from src.config.log_config import setup_logger
from wsgi import app_with_static

logger = setup_logger('app')
if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    logger.info(f"Сервер запущен http://{host}:{port}/")
    serve(app_with_static, host=host, port=port, _quiet=True)
