import enum

from sqlalchemy import Column, DateTime, func, Integer, String, ForeignKey, Boolean, Enum, Table
from sqlalchemy.orm import relationship, declarative_mixin

from src.db.database import Base


class Type(enum.Enum):
    salad = 1
    soup = 2
    main_dish = 3
    dessert = 4
    drink = 5
    bakery = 6


@declarative_mixin
class Timestamp:
    created_at = Column(DateTime(True), server_default=func.now())
    updated_at = Column(DateTime(True), default=func.now(), onupdate=func.now(),
                        server_default=func.now())


class SARecipe(Timestamp, Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(100), unique=True, index=True, nullable=False)
    type = Column(Enum(Type))
    description = Column(String(1000), nullable=True)
    steps = Column(String(1000), nullable=True)
    photo = Column(String(1000), nullable=False, default="https://ppss.kr/wp-content/uploads/2017/08/"
                                                         "MC_SightWords-Some.jpg")
    likes = Column(Integer, default=0)
    tags = Column(String(1000), nullable=True, default="[]")
    is_active = Column(Boolean, default=True)

    author = relationship("SAUser", back_populates="recipes")


class SAUser(Timestamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(100), nullable=False)
    likes = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    recipes = relationship("SARecipe", back_populates="author")
