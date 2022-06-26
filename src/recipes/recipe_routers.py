from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.recipes import recipe_crud
from src.recipes.recipe_schemas import RecipeBase, Recipe
from src.users.oauth2 import get_current_active_user
from src.users.user_schemas import UserResponse

router = APIRouter(
    tags=["Recipes"],
    prefix="/recipe",
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Recipe)
def create_recipe(request: RecipeBase, db: Session = Depends(get_db),
                  current_user: UserResponse = Depends(get_current_active_user)):
    return recipe_crud.create_recipe(db, request, current_user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_recipe(recipe_id: int, db: Session = Depends(get_db),
                           current_user: UserResponse = Depends(get_current_active_user)):
    return recipe_crud.delete_my_recipe(db, recipe_id, current_user)


@router.put("/{id}", status_code=status.HTTP_200_OK)
def like_recipe(recipe_id: int, db: Session = Depends(get_db),
                         current_user: UserResponse = Depends(get_current_active_user)):
    return recipe_crud.like_recipe(db, recipe_id, current_user)
