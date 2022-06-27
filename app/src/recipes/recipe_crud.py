from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.db import models
from src.recipes.recipe_schemas import NewRecipe, UpdateRecipe
from src.users.user_schemas import UserResponse


def create_recipe(db: Session, request: NewRecipe, current_user: UserResponse):
    new_recipe = models.SARecipe(
        title=request.title,
        description=request.description,
        type=request.type,
        steps=request.steps,
        author_id=current_user.id
    )
    recipe = db.query(models.SARecipe).filter(models.SARecipe.title == new_recipe.title).first()
    if recipe:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Recipe with this title already exists")
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    user = db.query(models.SAUser).filter(models.SAUser.id == current_user.id).first()
    user.my_recipes_count += 1
    db.commit()
    db.refresh(user)
    return new_recipe


def update_my_recipe(db: Session, recipe_id: int, request: UpdateRecipe, current_user: UserResponse):
    recipe = db.query(models.SARecipe).filter(models.SARecipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with id {recipe_id} not found")
    if recipe.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can`t update other users recipes")
    if request.title:
        check_recipe_title = db.query(models.SARecipe).filter(models.SARecipe.title == request.title).first()
        if check_recipe_title:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Recipe with this title already exists")
        recipe.title = request.title
    if request.description:
        recipe.description = request.description
    if request.type:
        recipe.type = request.type
    if request.steps:
        recipe.steps = request.steps
    db.commit()
    db.refresh(recipe)
    return {"message": "Recipe updated"}


def like_recipe(db: Session, recipe_id: int, current_user: UserResponse):
    recipe = db.query(models.SARecipe).filter(models.SARecipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with id {recipe_id} not found")
    user = db.query(models.SAUser).filter(models.SAUser.id == current_user.id).first()
    if db.query(models.SALike).filter(models.SALike.user_id == user.id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already liked this recipe")
    like = models.SALike(user_id=user.id, recipe_id=recipe.id)
    db.add(like)
    db.commit()
    db.refresh(like)
    recipe.likes_count += 1
    db.commit()
    author = db.query(models.SAUser).filter(models.SAUser.id == recipe.author_id).first()
    author.likes_from_all_my_recipes += 1
    db.commit()
    db.refresh(recipe)
    return {"message": "Recipe liked"}


def add_favorite_recipe(db: Session, recipe_id: int, current_user: UserResponse):
    recipe = db.query(models.SARecipe).filter(models.SARecipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with id {recipe_id} not found")
    user = db.query(models.SAUser).filter(models.SAUser.id == current_user.id).first()
    if db.query(models.SAFavorite).filter(models.SAFavorite.user_id == user.id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already added this recipe to favorites")
    favorite = models.SAFavorite(user_id=user.id, recipe_id=recipe.id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return {"message": "Recipe added to favorites"}


def remove_recipe_from_favorites(db: Session, recipe_id: int, current_user: UserResponse):
    recipe = db.query(models.SARecipe).filter(models.SARecipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with id {recipe_id} not found")
    user = db.query(models.SAUser).filter(models.SAUser.id == current_user.id).first()
    if not db.query(models.SAFavorite).filter(models.SAFavorite.user_id == user.id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You don`t have any favorites yet")
    favorite = db.query(models.SAFavorite).filter(models.SAFavorite.user_id == user.id).first()
    if favorite.recipe_id != recipe.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You don`t have this recipe in favorites")
    db.query(models.SAFavorite).filter(models.SAFavorite.recipe_id == recipe.id).delete()
    db.commit()
    return {"message": "Recipe removed from favorites"}


def delete_my_recipe(db: Session, recipe_id: int, current_user: UserResponse):
    recipe = db.query(models.SARecipe).filter(models.SARecipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with id {recipe_id} not found")
    if recipe.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete only your recipes")
    user = db.query(models.SAUser).filter(models.SAUser.id == current_user.id).first()
    user.my_recipes_count -= 1
    user.likes_from_all_my_recipes -= recipe.likes_count
    db.commit()
    db.refresh(user)
    db.query(models.SALike).filter(models.SALike.recipe_id == recipe.id).delete()
    db.commit()
    db.query(models.SARecipe).filter(models.SARecipe.id == recipe.id).delete()
    db.commit()
    return {"message": "Recipe deleted"}


def get_recipe(db: Session, recipe_id: int):
    recipe = db.query(models.SARecipe).filter(models.SARecipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with id {recipe_id} not found")
    if not recipe.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe is not active")
    return recipe


def get_all_recipes(db: Session):
    recipes = db.query(models.SARecipe). \
        filter(models.SARecipe.is_active == True). \
        order_by(models.SARecipe.likes_count.desc()). \
        all()
    return recipes


def block_recipe(db: Session, recipe_id: int, current_user: UserResponse):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can`t block recipes")
    recipe = db.query(models.SARecipe).filter(models.SARecipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with id {recipe_id} not found")
    if not recipe.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe is already blocked")
    recipe.is_active = False
    db.commit()
    return {"message": "Recipe blocked"}


def unblock_recipe(db: Session, recipe_id: int, current_user: UserResponse):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can`t unblock recipes")
    recipe = db.query(models.SARecipe).filter(models.SARecipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with id {recipe_id} not found")
    if recipe.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe is not blocked")
    recipe.is_active = True
    db.commit()
    return {"message": "Recipe unblocked"}
