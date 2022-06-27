from fastapi import FastAPI

from src.db import models
from src.db.database import engine
from src.recipes import recipe_routers
from src.users import user_routers

description = """
Recipes_API helps you do awesome stuff. 🚀
## Recipes
You can:
* create recipe
* read recipe
* update recipe
* delete recipe
* like recipe
* add recipe to favorite
* remove recipe from favorite
* block recipe (if you are admin)
* unblock recipe (if you are admin)

## Users
You can:
* create user
* authenticate user
* read user
* update user
* delete user
* block user (if you are admin)
* unblock user (if you are admin)


"""

app = FastAPI(
    title="FastAPI_Recipes",
    description=description,
    version="0.0.1",

)

models.Base.metadata.create_all(bind=engine)

app.include_router(user_routers.router_auth)
app.include_router(user_routers.router)
app.include_router(recipe_routers.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
