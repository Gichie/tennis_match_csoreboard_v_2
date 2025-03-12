from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.config.config import DATABASE_URI

# Настройка подключения к базе данных
engine = create_engine(DATABASE_URI, echo=True)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
# Функция для получения сессии
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
