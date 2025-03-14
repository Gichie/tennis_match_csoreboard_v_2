import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.player import Player
from services.exceptions import DatabaseError, PlayerNotFound

logger = logging.getLogger(__name__)


class PlayerService:
    """
    Provides services for managing players.

    This class encapsulates the logic for creating, retrieving, and managing player data.
    """

    @staticmethod
    def create_player(name: str) -> Player:
        """
        Creates a new player object.

        :param name: The name of the player.
        :return: The newly created Player object.
        """
        player = Player(name=name.strip())
        return player

    @staticmethod
    def get_or_create_player_id(db: Session, name: str) -> int:
        """
        Retrieves the ID of an existing player by name, or creates a new player if one doesn't exist.

        :param db: The SQLAlchemy session.
        :param name: The name of the player.
        :return: The ID of the player.
        :raises DatabaseError: If a database error occurs during retrieval or creation.
        """
        try:
            player = db.query(Player).filter(Player.name.ilike(name)).first()
            if not player:
                player = PlayerService.create_player(name)
                db.add(player)
                db.commit()
                db.refresh(player)
            return player.id
        except SQLAlchemyError as e:
            logger.error('Failed to get or create player id')
            raise DatabaseError('Failed to get or create player id')

    @staticmethod
    def get_name(db: Session, player_id: int) -> str:
        """
        Retrieves the name of a player by their ID.

        :param db: The SQLAlchemy session.
        :param player_id: The ID of the player.
        :return: The name of the player.
        :raises PlayerNotFound: If a player with the given ID is not found.
        """
        player = db.query(Player).get(player_id)
        if player:
            return player.name
        else:
            logger.error("Error getting name")
            raise PlayerNotFound(player_id)
