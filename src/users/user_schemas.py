from typing import Optional

from pydantic import BaseModel


class LoginUser(BaseModel):
    username: str
    password: str


class NewUser(LoginUser):
    pass


class LoginUserRequest(BaseModel):
    user: LoginUser


class NewUserRequest(BaseModel):
    user: NewUser


class User(LoginUser):
    likes: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


class UserInResponse(BaseModel):
    username: str
    likes: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserInResponse


class UpdateUser(BaseModel):
    username: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True


class UpdateUserRequest(BaseModel):
    user: Optional[UpdateUser] = None


class UpdateUserByAdmin(UpdateUser):
    likes: Optional[int] = None
    is_admin: Optional[bool] = None


class UpdateUserByAdminRequest(BaseModel):
    user: Optional[UpdateUserByAdmin] = None


class ProfileUser(BaseModel):
    username: str
    likes: int
    favorites: int
    recipes: int
    comments: int

    class Config:
        orm_mode = True


class ProfileUserResponse(BaseModel):
    profile: ProfileUser
