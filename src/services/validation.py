import re

MAX_LENGTH = 128
NAME_PATTERN = re.compile(r'^[^\W\d_]+(?:-[^\W\d_]+)*$', re.UNICODE)
MIN_PAGE = 1


class Validation:
    @staticmethod
    def player_names(player1_name: str, player2_name: str) -> dict:
        errors = {}

        player_name1 = player1_name.lower()
        player_name2 = player2_name.lower()

        if not player_name1:
            errors["player1"] = "Имя первого игрока не может быть пустым"
        if not player_name2:
            errors["player2"] = "Имя второго игрока не может быть пустым"

        if player_name1 == player_name2:
            errors["duplicate"] = "Имена игроков должны быть разными"

        def is_valid_name(name):
            return all(NAME_PATTERN.match(word) for word in name.split())

        if not is_valid_name(player_name1):
            errors["letters1"] = "Имя первого игрока должно состоять из букв и может содержать дефис между буквами"
        if not is_valid_name(player_name2):
            errors["letters2"] = "Имя второго игрока должно состоять из букв и может содержать дефис между буквами"

        if len(player_name1) > MAX_LENGTH:
            errors["max_length1"] = f"Длинна имени первого игрока не должна превышать {MAX_LENGTH} символов"
        if len(player_name2) > MAX_LENGTH:
            errors["max_length2"] = f"Длинна имени второго игрока не должна превышать {MAX_LENGTH} символов"

        return errors

    @staticmethod
    def correct_page(page, total_matches, per_page):
        last_page = total_matches // per_page + 1
        if page < MIN_PAGE:
            return MIN_PAGE
        elif page > last_page:
            return last_page
        return page
