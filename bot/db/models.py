"""DB Models"""

from sqlalchemy import (
    Integer,
    String,
    Text,
    Column,
    ForeignKey,
    BigInteger,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BotService(Base):
    __tablename__ = "bot_services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)

    user_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
