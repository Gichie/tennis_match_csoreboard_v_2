import json
from urllib.parse import parse_qs

from sqlalchemy.orm import Session

from myapp.database.session import get_db
from myapp.services.match_service import MatchService
from myapp.services.player_service import PlayerService
from myapp.views.match_view import MatchView


class MatchController:
    def __init__(self):
        self.view = MatchView()

    def new_match_form(self, environ, start_response):
        # Отображаем форму для создания матча
        response_body = self.view.render_new_match_form()
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [response_body.encode('utf-8')]

    def create_match(self, environ, start_response):
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            # Читаем сырые байты из входного потока и декодируем байты в строку (UTF-8)
            post_data_bytes = environ['wsgi.input'].read(content_length).decode('utf-8')
            # Парсим параметры с учетом URL-кодирования
            params = parse_qs(post_data_bytes)

            player1_name = params.get('player1', [''])[0]
            player2_name = params.get('player2', [''])[0]

            db: Session = next(get_db())

            # Получаем или создаем игроков
            # Используем сервисы
            player1 = PlayerService.get_or_create(db, player1_name)
            player2 = PlayerService.get_or_create(db, player2_name)
            new_match = MatchService.create_match(db, player1, player2)

            db.add(new_match)
            db.commit()
            db.refresh(new_match)

            # Редирект на страницу матча
            headers = [
                ('Location', f'/match-score?uuid={new_match.uuid}'),
                ('Content-Type', 'text/plain')
            ]
            start_response('302 Found', headers)
            return [b'Redirecting...']
        except Exception as e:
            # Обработка ошибок
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [b'Internal Server Error']

    def match_score(self, environ, start_response):
        # Получаем UUID из параметров запроса
        query = parse_qs(environ.get('QUERY_STRING', ''))
        match_uuid = query.get('uuid', [''])[0]

        db: Session = next(get_db())
        match = MatchService.get_match_by_uuid(db, match_uuid)  # Используем MatchService

        if not match:
            return self._not_found(start_response)

        if environ['REQUEST_METHOD'] == 'POST':
            return self._handle_score_update(environ, start_response, match, db)

        return self._render_score_page(start_response, match)

    def _handle_score_update(self, environ, start_response, match, db):
        try:
            # Парсим POST данные
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            post_data = environ['wsgi.input'].read(content_length).decode('utf-8')
            params = parse_qs(post_data)

            # Определяем, какой игрок получил очко
            if 'player1_point' in params:
                player_num = 1
            elif 'player2_point' in params:
                player_num = 2
            else:
                return self._bad_request(start_response)

            # Обновляем счёт
            MatchService.add_point(db, match, player_num)  # Используем MatchService

            # Проверяем завершение матча
            if MatchService.is_match_finished(match):  # Используем MatchService
                match.winner_id = player_num
                db.commit()
                return self._render_final_score(start_response, match)

            db.commit()
            return self._render_score_page(start_response, match)

        except Exception as e:
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [b'Error processing request']

    def _render_score_page(self, start_response, match):
        db: Session = next(get_db())
        player1_name = PlayerService.get_name(db, match.player1_id)  # Используем MatchService
        player2_name = PlayerService.get_name(db, match.player2_id)  # Используем MatchService

        try:
            # Принудительно загружаем Score из БД
            score_data = json.loads(match.score) if match.score else {"sets": []}
        except json.JSONDecodeError:
            score_data = {"sets": []}

        context = {
            "match": {
                "UUID": match.uuid,
                "Score": match.score,
                "Player1": match.player1_id,
                "Player2": match.player2_id,
                "Winner": match.winner_id
            },
            "player1": player1_name,
            "player2": player2_name,
            "score": MatchService.get_score_data(match),  # Используем MatchService
            "finished": False
        }

        if not isinstance(context["score"], dict):
            context["score"] = {"sets": []}

        response_body = self.view.render_match_score(context)
        headers = [('Content-Type', 'text/html; charset=utf-8')]
        start_response('200 OK', headers)
        return [response_body.encode('utf-8')]  # Обязательное кодирование

    def _render_final_score(self, start_response, match):
        db: Session = next(get_db())
        winner_name = PlayerService.get_name(db, match.winner_id)

        context = {
            "match": match,
            "player1": PlayerService.get_name(db, match.player1_id),
            "player2": PlayerService.get_name(db, match.player2_id),
            "winner": winner_name,
            "finished": True
        }

        response_body = self.view.render_match_score(context)
        headers = [('Content-Type', 'text/html; charset=utf-8')]
        start_response('200 OK', headers)
        return [response_body.encode('utf-8')]

    def _not_found(self, start_response):
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Match not found']

    def _bad_request(self, start_response):
        start_response('400 Bad Request', [('Content-Type', 'text/plain')])
        return [b'Invalid request']
