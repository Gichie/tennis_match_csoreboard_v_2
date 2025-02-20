from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from myapp.config import DATABASE_URI

# Настройка подключения к базе данных
engine = create_engine(DATABASE_URI)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

