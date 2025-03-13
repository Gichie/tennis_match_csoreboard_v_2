import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.config.config import DATABASE_URI

logger = logging.getLogger(__name__)

# Настройка подключения к базе данных


logger.info("Initializing database connection")
engine = create_engine(DATABASE_URI, echo=False)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
# Функция для получения сессии
def get_db() -> Session:
    db = SessionLocal()
    logger.debug("Database session created")
    try:
        yield db
    except Exception as e:
        logger.error("Database session error: %s", str(e), exc_info=True)
        raise
    finally:
        db.close()
        logger.debug("Database session closed")
