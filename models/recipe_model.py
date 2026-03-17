import datetime

from sqlalchemy import DateTime, Integer, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from db.database import Base


class Recipes(Base):
    __tablename__ = 'recipes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(100, charset='utf8mb3', collation='utf8mb3_unicode_ci'), nullable=False)
    making_time: Mapped[str] = mapped_column(VARCHAR(100, charset='utf8mb3', collation='utf8mb3_unicode_ci'), nullable=False)
    serves: Mapped[str] = mapped_column(VARCHAR(100, charset='utf8mb3', collation='utf8mb3_unicode_ci'), nullable=False)
    ingredients: Mapped[str] = mapped_column(VARCHAR(300, charset='utf8mb3', collation='utf8mb3_unicode_ci'), nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
