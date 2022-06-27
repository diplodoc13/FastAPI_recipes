from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.recipes import recipe_crud
from src.recipes.recipe_schemas import NewRecipe, RecipeResponse, RecipeFullResponse, UpdateRecipe
from src.users.oauth2 import get_current_active_user
from src.users.user_schemas import UserResponse

router = APIRouter(
    tags=["Recipes"],
    prefix="/recipe",
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RecipeResponse)
def create_recipe(request: NewRecipe, db: Session = Depends(get_db),
                  current_user: UserResponse = Depends(get_current_active_user)):
    return recipe_crud.create_recipe(db, request, current_user)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=RecipeFullResponse)
def show_recipe(id: int, db: Session = Depends(get_db),
                current_user: UserResponse = Depends(get_current_active_user)):
    return recipe_crud.get_recipe(db, id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_recipe(recipe_id: int, db: Session = Depends(get_db),
                     current_user: UserResponse = Depends(get_current_active_user)):
    return recipe_crud.delete_my_recipe(db, recipe_id, current_user)


@router.put("/{id}", status_code=status.HTTP_200_OK)
def like_recipe(recipe_id: int, db: Session = Depends(get_db),
                current_user: UserResponse = Depends(get_current_active_user)):
    return recipe_crud.like_recipe(db, recipe_id, current_user)


@router.put("/{id}/favorite", status_code=status.HTTP_200_OK)
def add_favorite_recipe(recipe_id: int, db: Session = Depends(get_db),
                        current_user: UserResponse = Depends(get_current_active_user)):
    return recipe_crud.add_favorite_recipe(db, recipe_id, current_user)


@router.put("/{id}/unfavorite", status_code=status.HTTP_200_OK)
def remove_recipe_from_favorites(recipe_id: int, db: Session = Depends(get_db),
                                 current_user: UserResponse = Depends(get_current_active_user)):
    return recipe_crud.remove_recipe_from_favorites(db, recipe_id, current_user)


@router.put("/{id}/update", status_code=status.HTTP_200_OK)
def update_my_recipe(recipe_id: int, request: UpdateRecipe, db: Session = Depends(get_db),
                     current_user: UserResponse = Depends(get_current_active_user)):
    return recipe_crud.update_my_recipe(db, recipe_id, request, current_user)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[RecipeResponse])
def show_all_recipes(db: Session = Depends(get_db),
                     current_user: UserResponse = Depends(get_current_active_user)):
    return recipe_crud.get_all_recipes(db)


# administration functions

@router.put("/block/{id}", status_code=status.HTTP_200_OK)
def block_recipe(recipe_id: int, db: Session = Depends(get_db),
                 current_user: UserResponse = Depends(get_current_active_user)):
    return recipe_crud.block_recipe(db, recipe_id, current_user)


@router.put("/unblock/{id}", status_code=status.HTTP_200_OK)
def unblock_recipe(recipe_id: int, db: Session = Depends(get_db),
                   current_user: UserResponse = Depends(get_current_active_user)):
    return recipe_crud.unblock_recipe(db, recipe_id, current_user)
