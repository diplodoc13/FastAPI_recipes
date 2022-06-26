from fastapi import FastAPI

from src.db import models
from src.db.database import engine
from src.users import user_routers

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(user_routers.router_auth)
app.include_router(user_routers.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
