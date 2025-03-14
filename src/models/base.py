from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    This class inherits from `DeclarativeBase` and provides a common base
    for defining database tables.  It includes an `id` column as the primary key.
    """
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
