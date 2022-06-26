from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.db import models
from src.recipes.recipe_schemas import RecipeBase
from src.users.user_schemas import UserResponse


def create_recipe(db: Session, request: RecipeBase, current_user: UserResponse):
    new_recipe = models.SARecipe(
        title=request.title,
        description=request.description,
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


# def delete_my_recipe(db: Session, recipe_id: int, current_user: UserResponse):
#     recipe = db.query(models.SARecipe).filter(models.SARecipe.id == recipe_id).first()
#     if not recipe:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with id {recipe_id} not found")
#     if recipe.author_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't delete other user's recipe")
#     db.query(models.SALike).filter(models.SALike.recipe_id == recipe.id).delete()
#     db.query(models.SARecipe).filter(models.SARecipe.id == recipe.id).delete()
#     user = db.query(models.SAUser).filter(models.SAUser.id == current_user.id).first()
#     user.my_recipes_count -= 1
#     db.commit()
#     db.refresh(user)
#     return {"message": "Recipe deleted"}

# def delete_my_recipe(db: Session, recipe_id: int, current_user: UserResponse):
#     recipe = db.query(models.SARecipe).filter(models.SARecipe.id == recipe_id).first()
#     if not recipe:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with id {recipe_id} not found")
#     user = db.query(models.SAUser).filter(models.SAUser.id == current_user.id).first()
#     if not db.query(models.SALike).filter(models.SALike.user_id == user.id).first():
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You haven't liked this recipe")
#     db.query(models.SALike).filter(models.SALike.user_id == user.id).delete()
#     db.commit()
#     db.refresh(recipe)
#     recipe.likes_count -= 1
#     db.commit()
#     db.refresh(recipe)
#     user.my_recipes_count -= 1
#     db.commit()
#     db.refresh(user)
#     return {"message": "Recipe deleted"}

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


