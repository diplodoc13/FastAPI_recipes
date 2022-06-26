from typing import Optional

from pydantic import BaseModel

from src.users.user_schemas import ProfileUser


class Recipe(BaseModel):
    title: str
    description: str
    type: str
    tagList: Optional[list[str]] = []
    likes: int
    is_active: bool
    author_id: ProfileUser

    class Config:
        orm_mode = True


class GetRecipes(BaseModel):
    recipes: list[Recipe]

    class Config:
        orm_mode = True

class CreateRecipe(BaseModel):
    title: str
    description: str
    type: str
    tagList: Optional[list[str]] = []

    class Config:
        orm_mode = True

class CreateRecipeRequest(BaseModel):
    recipe: CreateRecipe

    class Config:
        orm_mode = True

class CreateRecipeResponse(BaseModel):
    recipe: Recipe

    class Config:
        orm_mode = True

class GetRecipe(BaseModel):
    recipe: Recipe

    class Config:
        orm_mode = True

class ChangeRecipe(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    tagList: Optional[list[str]] = None

    class Config:
        orm_mode = True

class UpdateAricleRequest(BaseModel):
    recipe: ChangeRecipe

    class Config:
        orm_mode = True

class Comment(BaseModel):
    id: int
    content: str
    author_id: ProfileUser

    class Config:
        orm_mode = True


class GetCommentsResponse(BaseModel):
    comments: list[Comment]


class CreateCommentContent(BaseModel):
    content: str


class CreateComment(BaseModel):
    comment: CreateCommentContent



class GetCommentResponse(BaseModel):
    comment: Comment



class GetTags(BaseModel):
    tags: list[str]

    class Config:
        orm_mode = True