import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config.config import DATABASE_URI
from config.log_config import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

# Database connection setup

logger.info("Initializing database connection")
engine = create_engine(DATABASE_URI, echo=False)

# Creating a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
# Функция для получения сессии
def get_db() -> Session:
    """
    Provides a database session within a context manager.

    :return: A SQLAlchemy Session object.
    :raises Exception: If any error occurs during session handling.
    """
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
