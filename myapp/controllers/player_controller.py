from sqlalchemy.orm import Session

from myapp.database.session import get_db
from myapp.models.player import Player


class PlayerController:
    def create_player(self, name: str):
        with get_db() as db:
            new_player = Player(Name=name)
            db.add(new_player)
            db.commit()
            db.refresh(new_player)
            return new_player

    def get_player_by_name(self, name: str):
        with get_db() as db:
            return db.query(Player).filter(Player.name == name).first()
