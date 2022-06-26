from sqlalchemy.orm import Session

from src.db import models
from src.users.oauth2 import get_password_hash
from src.users.user_schemas import NewUser


def create_user(db: Session, request: NewUser):
    user = models.SAUser(username=request.username, hashed_password=get_password_hash(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user