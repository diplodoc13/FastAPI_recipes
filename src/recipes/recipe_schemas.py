from typing import Optional

from pydantic import BaseModel

class RecipeBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True

class Recipe(RecipeBase):
    id: int



