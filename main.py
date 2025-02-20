from waitress import serve
from wsgi import app_with_static

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    print(f"Сервер запущен http://{host}:{port}/")
    serve(app_with_static, host=host, port=port, _quiet=True)
