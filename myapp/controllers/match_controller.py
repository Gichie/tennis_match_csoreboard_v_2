import json

from myapp.models.models import Player, Match
from myapp.database.session import get_db
from myapp.views.match_view import MatchView
import uuid
from sqlalchemy.orm import Session
from urllib.parse import parse_qs


class MatchController:
    def __init__(self):
        self.view = MatchView()

    def new_match_form(self, environ, start_response):
        # Отображаем форму для создания матча
        response_body = self.view.render_new_match_form()
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [response_body.encode('utf-8')]

    def create_match(self, environ, start_response):
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        # Читаем сырые байты из входного потока и декодируем байты в строку (UTF-8)
        post_data_bytes = environ['wsgi.input'].read(content_length).decode('utf-8')
        # Парсим параметры с учетом URL-кодирования
        params = parse_qs(post_data_bytes)

        player1_name = params.get('player1', [''])[0]
        player2_name = params.get('player2', [''])[0]

        db: Session = next(get_db())

        # Получаем или создаем игроков
        player1 = Player.get_or_create(db, player1_name)
        player2 = Player.get_or_create(db, player2_name)

        # Создаем матч
        new_match = Match(
            UUID=str(uuid.uuid4()),
            Player1=player1.ID,
            Player2=player2.ID,
            Winner=None,
            Score=json.dumps({"sets": []})  # Явная сериализация
        )

        db.add(new_match)
        db.commit()
        db.refresh(new_match)

        # Редирект на страницу матча
        headers = [
            ('Location', f'/match-score?uuid={new_match.UUID}'),
            ('Content-Type', 'text/plain')
        ]
        start_response('302 Found', headers)
        return [b'Redirecting...']

    def match_score(self, environ, start_response):
        # Получаем UUID из параметров запроса
        query = parse_qs(environ.get('QUERY_STRING', ''))
        match_uuid = query.get('uuid', [''])[0]

        db: Session = next(get_db())
        match = db.query(Match).filter(Match.UUID == match_uuid).first()

        if not match:
            return self._not_found(start_response)

        if environ['REQUEST_METHOD'] == 'POST':
            return self._handle_score_update(environ, start_response, match, db)

        return self._render_score_page(start_response, match)

    def _handle_score_update(self, environ, start_response, match, db):
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
        match.add_point(player_num)

        # Проверяем завершение матча
        if self._is_match_finished(match):
            match.Winner = player_num
            db.commit()
            return self._render_final_score(start_response, match)

        db.commit()
        return self._render_score_page(start_response, match)

    def _is_match_finished(self, match):
        # Здесь должна быть логика проверки завершения матча
        # Для примера: матч заканчивается после 4 очков
        print(f"Score type: {type(match.score_data)}, Content: {match.score_data}")
        score = match.score_data
        last_game = score['sets'][-1][-1] if score['sets'] else {}
        return any(v >= 4 for v in last_game.values())

    def _render_score_page(self, start_response, match):
        db: Session = next(get_db())
        player1 = db.query(Player).get(match.Player1)
        player2 = db.query(Player).get(match.Player2)

        try:
            # Принудительно загружаем Score из БД
            score_data = json.loads(match.Score) if match.Score else {"sets": []}
        except json.JSONDecodeError:
            score_data = {"sets": []}

        context = {
            "match": {
                "UUID": match.UUID,
                "Score": match.Score,
                "Player1": match.Player1,
                "Player2": match.Player2,
                "Winner": match.Winner
            },
            "player1": player1.Name if player1 else "Unknown",
            "player2": player2.Name if player2 else "Unknown",
            "score": score_data
        }

        if not isinstance(context["score"], dict):
            context["score"] = {"sets": []}

        response_body = self.view.render_match_score(context)
        headers = [('Content-Type', 'text/html; charset=utf-8')]
        start_response('200 OK', headers)
        return [response_body.encode('utf-8')]  # Обязательное кодирование

    def _render_final_score(self, start_response, match):
        db: Session = next(get_db())
        winner = db.query(Player).get(match.Winner)

        context = {
            "match": match,
            "player1": self._get_player_name(match.Player1),
            "player2": self._get_player_name(match.Player2),
            "winner": winner.Name if winner else "Unknown",
            "finished": True
        }

        response_body = self.view.render_match_score(context)
        headers = [('Content-Type', 'text/html; charset=utf-8')]
        start_response('200 OK', headers)
        return [response_body.encode('utf-8')]

    def _get_player_name(self, player_id):
        db: Session = next(get_db())
        player = db.query(Player).get(player_id)
        return player.Name if player else 'Unknown'

    def _not_found(self, start_response):
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Match not found']

    def _bad_request(self, start_response):
        start_response('400 Bad Request', [('Content-Type', 'text/plain')])
        return [b'Invalid request']
