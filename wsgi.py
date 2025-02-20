import os

from whitenoise import WhiteNoise

from myapp.controllers.home_controller import HomeController
from myapp.controllers.match_controller import MatchController

# Путь к статическим файлам
static_path = os.path.join(os.path.dirname(__file__), 'myapp/static')


def application(environ, start_response):
    path = environ.get('PATH_INFO', '')
    method = environ.get('REQUEST_METHOD', 'GET')

    if path == '/index' or path == '/':  # Главная страница
        controller = HomeController()
        return controller.index(environ, start_response)
    elif path == '/new-match':
        controller = MatchController()
        if method == 'POST':
            return controller.create_match(environ, start_response)
        else:
            return controller.new_match_form(environ, start_response)
    elif path == '/match-score':
        controller = MatchController()
        return controller.match_score(environ, start_response)
    else:
        # Возвращаем 404, если маршрут не найден
        status = '404 Not Found'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b"404 Not Found"]


app_with_static = WhiteNoise(application, root=static_path, prefix='/static')
