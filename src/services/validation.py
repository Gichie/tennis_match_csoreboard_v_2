from config.config import NAME_PATTERN, MAX_LENGTH, MIN_PAGE


class Validation:
    """
    A class containing static methods for validating player names and page numbers.
    """

    @staticmethod
    def player_names(player1_name: str, player2_name: str) -> dict[str, str]:
        """
        Validates player names to ensure they meet specific criteria.

        :param player1_name: The name of the first player.
        :param player2_name: The name of the second player.
        :return: A dictionary containing error messages if validation fails.
                 Returns an empty dictionary if both names are valid.
        """
        errors = {}

        player_name1 = player1_name.lower()
        player_name2 = player2_name.lower()

        if not player_name1:
            errors["player1"] = "The first player name cannot be empty."
        if not player_name2:
            errors["player2"] = "The second player name cannot be empty."

        if player_name1 == player_name2:
            errors["duplicate"] = "Player names must be different"

        def is_valid_name(name: str) -> bool:
            return all(NAME_PATTERN.match(word) for word in name.split())

        if not is_valid_name(player_name1):
            errors["letters1"] = "First player's name must consist of letters and may contain a hyphen between letters"
        if not is_valid_name(player_name2):
            errors["letters2"] = "Second player's name must consist of letters and may contain a hyphen between letters"

        if len(player_name1) > MAX_LENGTH:
            errors["max_length1"] = f"The first player's name must not exceed {MAX_LENGTH} characters."
        if len(player_name2) > MAX_LENGTH:
            errors["max_length2"] = f"The second player's name must not exceed {MAX_LENGTH} characters."

        return errors

    @staticmethod
    def correct_page(page: int, total_matches: int, per_page: int) -> int:
        """
        Corrects the page number to ensure it falls within the valid range.

        :param page: The page number to validate.
        :param total_matches: The total number of matches.
        :param per_page: The number of matches per page.
        :return: The corrected page number if it was out of range, otherwise the original page number.
        """
        last_page = total_matches // per_page + 1
        if page < MIN_PAGE:
            return MIN_PAGE
        elif page > last_page:
            return last_page
        return page
