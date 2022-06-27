from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.db import models
from src.users.oauth2 import get_password_hash
from src.users.user_schemas import NewUser, UserResponse, UpdateUser


def create_user(db: Session, request: NewUser):
    user = models.SAUser(username=request.username, hashed_password=get_password_hash(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_me(db: Session, request: UpdateUser, current_user: UserResponse):
    user = db.query(models.SAUser).filter(models.SAUser.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {current_user.id} not found")
    if request.username:
        user.username = request.username
    db.commit()
    db.refresh(user)
    return user


def delete_me(db: Session, current_user: UserResponse):
    user = db.query(models.SAUser).filter(models.SAUser.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {current_user.id} not found")
    if user.is_active:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="You must deactivate your account before delete")
    db.delete(user)
    db.commit()
    return {"message": "Your account has been deleted"}


def deactivate_me(db: Session, current_user: UserResponse):
    user = db.query(models.SAUser).filter(models.SAUser.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {current_user.id} not found")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You are already blocked")
    user.is_active = False
    db.commit()
    db.refresh(user)
    return {"message": "Your account deactivated"}


def get_user(db: Session, user_id: int):
    user = db.query(models.SAUser).filter(models.SAUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user


def get_users(db: Session, ):
    users = db.query(models.SAUser). \
        filter(models.SAUser.is_active == True). \
        order_by(models.SAUser.my_recipes_count.desc()). \
        order_by(models.SAUser.likes_from_all_my_recipes.desc()). \
        all()
    return users


def block_user(db: Session, user_id: int, current_user: UserResponse):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can`t block user")
    user = db.query(models.SAUser).filter(models.SAUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already blocked")
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user


def unblock_user(db: Session, user_id: int, current_user: UserResponse):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can`t unblock user")
    user = db.query(models.SAUser).filter(models.SAUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    if user.is_active:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is active now")
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user
