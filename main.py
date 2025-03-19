import logging

from waitress import serve

from wsgi import app_with_static

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    logger.info(f"The server is running http://{host}:{port}/")
    serve(app_with_static, host=host, port=port)
    logger.info("The server has stopped")
