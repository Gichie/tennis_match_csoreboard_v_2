from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import logging

from myapp.models.player import Player


logger = logging.getLogger(__name__)


class PlayerService:
    @staticmethod
    def get_or_create(db: Session, name: str) -> Player:
        try:
            # Проверяем валидность имени
            if not name or not isinstance(name, str):
                raise ValueError("Invalid player name")

            player = db.query(Player).filter(Player.name.ilike(name)).first()
            if not player:
                player = Player(name=name.strip())
                db.add(player)
                db.commit()
                db.refresh(player)
            return player

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise

    @staticmethod
    def get_name(db: Session, player_id: int) -> str:
        player = db.query(Player).get(player_id)
        return player.name if player else 'Unknown'
