from sqlalchemy import Column, DateTime, func, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_mixin

from src.db.database import Base


@declarative_mixin
class Timestamp:
    created_at = Column(DateTime(True), server_default=func.now())
    updated_at = Column(DateTime(True), default=func.now(), onupdate=func.now(),
                        server_default=func.now())


class SARecipe(Timestamp, Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(100), unique=True, index=True, nullable=False)
    type = Column(String(1000), nullable=False)
    description = Column(String(1000), nullable=True)
    steps = Column(String(1000), nullable=False)
    photo = Column(String(1000), nullable=False, default="https://ppss.kr/wp-content/uploads/2017/08/"
                                                         "MC_SightWords-Some.jpg")
    likes_count = Column(Integer, default=0)
    tags = Column(String(1000), nullable=True, default="[]")
    is_active = Column(Boolean, default=True)

    author = relationship("SAUser", back_populates="recipes")
    likes = relationship("SALike", back_populates="recipe")
    favorites = relationship("SAFavorite", back_populates="recipe")


class SAUser(Timestamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(100), nullable=False)
    likes_from_all_my_recipes = Column(Integer, default=0)
    my_recipes_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    recipes = relationship("SARecipe", back_populates="author")
    likes = relationship("SALike", back_populates="user")
    favorites = relationship("SAFavorite", back_populates="user")


class SALike(Timestamp, Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))

    user = relationship("SAUser", back_populates="likes")
    recipe = relationship("SARecipe", back_populates="likes")


class SAFavorite(Timestamp, Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))

    user = relationship("SAUser", back_populates="favorites")
    recipe = relationship("SARecipe", back_populates="favorites")
