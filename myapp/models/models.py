import json

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

from myapp.config import DATABASE_URI

engine = create_engine(DATABASE_URI, echo=True)

# Базовый класс для моделей
Base = declarative_base()


class Player(Base):
    __tablename__ = 'Players'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False, index=True)

    # Связь с таблицей Matches
    matches_as_player1 = relationship("Match", foreign_keys="Match.Player1")
    matches_as_player2 = relationship("Match", foreign_keys="Match.Player2")
    matches_as_winner = relationship("Match", foreign_keys="Match.Winner")

    @classmethod
    def get_or_create(cls, db: Session, name: str):
        player = db.query(cls).filter(cls.Name == name).first()
        if not player:
            player = cls(Name=name)
            db.add(player)
            db.commit()
            db.refresh(player)
        return player


# Модель для таблицы Matches
class Match(Base):
    __tablename__ = 'Matches'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    UUID = Column(String(36), nullable=False, unique=True)
    Player1 = Column(Integer, ForeignKey('Players.ID'), nullable=False)
    Player2 = Column(Integer, ForeignKey('Players.ID'), nullable=False)
    Winner = Column(Integer, ForeignKey('Players.ID'), nullable=True)
    Score = Column(String(1000), nullable=False)



    @property
    def score_data(self):
        """Десериализуем JSON из строки."""
        try:
            return json.loads(self.Score) if self.Score else {"sets": []}
        except (TypeError, json.JSONDecodeError):
            return {"sets": []}

    @score_data.setter
    def score_data(self, value):
        """Сериализуем JSON в строку."""
        self.Score = json.dumps(value, ensure_ascii=False)

    def add_point(self, player_num: int):
        """Добавляет очко указанному игроку (1 или 2)"""
        score = self.score_data
        # Здесь должна быть логика подсчёта очков по правилам тенниса
        # Для примера: упрощённая версия
        current_set = score['sets'][-1] if score['sets'] else []

        if len(current_set) == 0 or current_set[-1] in ('player1', 'player2'):
            current_set.append({'player1': 0, 'player2': 0})

        current_game = current_set[-1]
        current_game[f'player{player_num}'] += 1

        # Обновляем данные
        if not score['sets']:
            score['sets'].append([])
        score['sets'][-1] = current_set
        self.score_data = score


@event.listens_for(Match, 'before_insert')
def set_default_score(mapper, connection, target):
    if not target.Score:
        target.Score = json.dumps({"sets": []}, ensure_ascii=False)
