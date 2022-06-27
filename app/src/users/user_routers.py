from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.users import user_crud
from src.users.oauth2 import Token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_current_active_user, get_current_user
from src.users.user_schemas import NewUser, UserResponse, ShowUser, UpdateUser

router = APIRouter(
    tags=["Users"],
    prefix="/users",
)

router_auth = APIRouter(
    tags=["Authentication"]
)


@router_auth.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(request: NewUser, db: Session = Depends(get_db)):
    return user_crud.create_user(db, request)


@router.put("/me/deactivate", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_me(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_active_user)):
    return user_crud.deactivate_me(db, current_user)


@router.delete("/me/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return user_crud.delete_me(db, current_user)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.put("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def update_me(request: UpdateUser, db: Session = Depends(get_db),
              current_user: UserResponse = Depends(get_current_user)):
    return user_crud.update_me(db, current_user, request)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def read_user(id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_active_user)):
    return user_crud.get_user(db, id)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_active_user)):
    return user_crud.get_users(db)


# administration functions

@router.put("/block/{id}", status_code=status.HTTP_200_OK, response_model=ShowUser)
def block_user(id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_active_user)):
    return user_crud.block_user(db, id, current_user)


@router.put("/unblock/{id}", status_code=status.HTTP_200_OK, response_model=ShowUser)
def unblock_user(id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_active_user)):
    return user_crud.unblock_user(db, id, current_user)
