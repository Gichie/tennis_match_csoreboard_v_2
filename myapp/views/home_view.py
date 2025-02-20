from jinja2 import Environment, FileSystemLoader
import os


class HomeView:
    def __init__(self):
        # Указываем путь к шаблонам
        template_path = os.path.join(os.path.dirname(__file__), '../templates')
        self.env = Environment(loader=FileSystemLoader(template_path))

    def render_home(self):
        # Загружаем шаблон главной страницы
        template = self.env.get_template('home.html')
        # Рендерим шаблон
        return template.render()
