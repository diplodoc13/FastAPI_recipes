import enum

from sqlalchemy import Column, DateTime, func, Integer, String, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship

from src.db.database import Base


class Type(enum.Enum):
    salad = 1
    soup = 2
    main_dish = 3
    dessert = 4
    drink = 5
    bakery = 6


class TimedBaseModel(Base):
    created_at = Column(DateTime(True), server_default=func.now())
    updated_at = Column(DateTime(True), default=func.now(), onupdate=func.now(),
                        server_default=func.now())


class SARecipe(TimedBaseModel):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), unique=True, index=True, nullable=False)
    type = Column(Enum(Type))
    description = Column(String(1000), nullable=True)
    steps = Column(String(1000), nullable=True)
    photo = Column(String(1000), nullable=False, default="https://ppss.kr/wp-content/uploads/2017/08/"
                                                         "MC_SightWords-Some.jpg")
    likes = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    author = relationship("SAUser", back_populates="resipes")
    favorites = relationship("SAFavorite", back_populates="recipe")
    tags = relationship("SATag", secondary="recipe_tags", back_populates="recipes")
    comments = relationship("SAComment", back_populates="recipe")


class SAFavorite(TimedBaseModel):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    user = relationship("SAUser", back_populates="favorites")
    recipe = relationship("SARecipe", back_populates="favorites")


class SATag(TimedBaseModel):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)

    recipes = relationship("SARecipe", back_populates="tags")


class SAComment(TimedBaseModel):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    content = Column(String(1000), nullable=False)

    user = relationship("SAUser", back_populates="comments")
    recipe = relationship("SARecipe", back_populates="comments")


class SAUser(TimedBaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    likes = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    resipes = relationship("SARecipe", back_populates="author")
    favorites = relationship("SAFavorite", back_populates="user")
    comments = relationship("SAComment", back_populates="user")
