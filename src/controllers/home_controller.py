from views.home_view import HomeView


class HomeController:
    def __init__(self):
        self.view = HomeView()

    def index(self, environ, start_response):
        response_body = self.view.render_home()
        status = '200 OK'
        headers = [('Content-Type', 'text/html')]
        start_response(status, headers)
        return [response_body.encode('utf-8')]