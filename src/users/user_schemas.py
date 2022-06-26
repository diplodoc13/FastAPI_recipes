from typing import Optional

from pydantic import BaseModel


class NewUser(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    is_active: bool
    is_admin: bool
    likes_from_all_my_recipes: int
    my_recipes_count: int

    class Config:
        orm_mode = True
