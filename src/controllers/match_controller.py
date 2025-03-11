import json
from urllib.parse import parse_qs

from src.database.session import get_db
from src.services import score_utils
from src.services.exceptions import NotFoundMatchError, InvalidGameStateError, PlayerNumberError, InvalidScoreError
from src.services.match_service import MatchService
from src.services.player_service import PlayerService
from src.services.validation import Validation
from src.views.match_view import MatchView


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
            post_data_bytes = environ['wsgi.input'].read(content_length).decode('utf-8')
            # Парсим параметры с учетом URL-кодирования
            params = parse_qs(post_data_bytes)

            player1_name = params.get('player1', [''])[0].strip()
            player2_name = params.get('player2', [''])[0].strip()
            validation_errors = Validation.player_names(player1_name, player2_name)
            if validation_errors:
                response_body = self.view.render_new_match_form(
                    player1_name=player1_name,
                    player2_name=player2_name,
                    errors=validation_errors
                )
                start_response('200 OK', [('Content-Type', 'text/html')])
                return [response_body.encode('utf-8')]

            with get_db() as db:
                player1_id = PlayerService.get_or_create_player_id(db, player1_name)
                player2_id = PlayerService.get_or_create_player_id(db, player2_name)
                new_match = MatchService.create_match(db, player1_id, player2_id)

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
            return self._handle_error(start_response, e, new_match.uuid, status='500 Internal Server Error')

    def match_score(self, environ, start_response):
        # Получаем UUID из параметров запроса
        query = parse_qs(environ.get('QUERY_STRING', ''))
        match_uuid = query.get('uuid', [''])[0]

        try:
            with get_db() as db:
                match = MatchService.get_match_by_uuid(db, match_uuid)

                try:
                    score = json.loads(match.score)
                except json.JSONDecodeError:
                    raise InvalidScoreError("Score data is corrupted")

                if environ['REQUEST_METHOD'] == 'POST':
                    return self._handle_score_update(environ, start_response, match, score, db)

                return self._render_score_page(start_response, match, score)

        except NotFoundMatchError as e:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [str(e).encode('utf-8')]

        except InvalidScoreError as e:
            return self._handle_error(start_response, e, match.uuid, status='400 Bad Request')

        except Exception as e:
            return self._handle_error(start_response, e, match.uuid, status='500 Internal Server Error')

    def _handle_score_update(self, environ, start_response, match, score, db):
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            post_data = environ['wsgi.input'].read(content_length).decode('utf-8')
            params = parse_qs(post_data)

            # Определяем, какой игрок получил очко
            player_num = MatchService.determine_player_number(params)
            # Обновляем счёт
            MatchService.add_point(db, match, score, player_num)

            # Проверяем завершение матча
            if score_utils.is_match_finished(score):
                return self._render_final_score(start_response, match)

            return self._render_score_page(start_response, match, score)

        except (InvalidGameStateError, PlayerNumberError) as e:
            return self._handle_error(start_response, e, match.uuid, status='400 Bad Request')

        except Exception as e:
            return self._handle_error(start_response, e, match.uuid, status='500 Internal Server Error')

    def _handle_error(self, start_response, exception, match_uuid=None, status='500 Internal Server Error'):
        error_message = str(exception)
        error_title = type(exception).__name__

        response_body = self.view.render_error_page({
            "error_title": error_title,
            "error_message": error_message,
            "match_uuid": match_uuid
        })

        headers = [('Content-Type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return [response_body.encode('utf-8')]

    def _render_score_page(self, start_response, match, score):
        with get_db() as db:
            context = {
                "uuid": match.uuid,
                "player1": PlayerService.get_name(db, match.player1_id),
                "player2": PlayerService.get_name(db, match.player2_id),
                "player1_points": score["player1"]["points"],
                "player1_games": score["player1"]["games"],
                "player1_sets": score["player1"]["sets"],
                "player2_points": score["player2"]["points"],
                "player2_games": score["player2"]["games"],
                "player2_sets": score["player2"]["sets"],
                "finished": False,
                "current_game_state": match.current_game_state
            }

            response_body = self.view.render_match_score(context)
            headers = [('Content-Type', 'text/html; charset=utf-8')]
            start_response('200 OK', headers)
            return [response_body.encode('utf-8')]  # Обязательное кодирование

    def _render_final_score(self, start_response, match):
        with get_db() as db:
            context = {
                "player1": PlayerService.get_name(db, match.player1_id),
                "player2": PlayerService.get_name(db, match.player2_id),
                "winner": PlayerService.get_name(db, match.winner_id),
                "player1_sets": json.loads(match.score)["player1"]["sets"],
                "player2_sets": json.loads(match.score)["player2"]["sets"],
            }
            response_body = self.view.render_final_score(context)
            headers = [('Content-Type', 'text/html; charset=utf-8')]
            start_response('200 OK', headers)
            return [response_body.encode('utf-8')]

    def _bad_request(self, start_response):
        start_response('400 Bad Request', [('Content-Type', 'text/plain')])
        return [b'Invalid request']
