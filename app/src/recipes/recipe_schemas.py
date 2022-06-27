from typing import Optional

from pydantic import BaseModel

from src.users.user_schemas import ShowUser


class NewRecipe(BaseModel):
    title: str
    description: str
    type: str
    steps: str

    class Config:
        orm_mode = True


class UpdateRecipe(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    steps: Optional[str] = None

    class Config:
        orm_mode = True


class RecipeResponse(BaseModel):
    id: int
    title: str
    description: str
    type: str
    likes_count: int
    photo: str
    is_active: bool
    author: ShowUser

    class Config:
        orm_mode = True


class RecipeFullResponse(RecipeResponse):
    steps: str

    class Config:
        orm_mode = True
