# FastAPI Recipes

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi&logoColor=white&color=ff1709&labelColor=gray)](https://fastapi.tiangolo.com//)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-005?style=flat-square)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-0001?style=flat-square)](https://pydantic-docs.helpmanual.io/)

[![Pydantic](https://wakatime.com/badge/user/499e43e9-6f16-4377-92ae-078c74517dbb/project/dc596292-46f6-4f63-86d9-ab0e8bdda598.svg)](https://wakatime.com/badge/user/499e43e9-6f16-4377-92ae-078c74517dbb/project/dc596292-46f6-4f63-86d9-ab0e8bdda598.svg)




Testing project.

In this project I use:
```
fastapi
pydantic
sqlalchemy
```

## Deployment local
1. Clone repository 
```
https://github.com/diplodoc13/FastAPI_recipes.git
```
2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/Scripts/activate 
```
3. Install the dependencies:
```
pip install -r requirements.txt
```
4. Create a `.env` (you can use `.env.example`), with your `SECRET` and `DATABASE_URL` in the same backend folder.

5. Install docker-compose and run the database container:
```
docker-compose -f docker-compose.yaml up
```

6. Run the application:
```
uvicorn main:app --reload
```
7. The app will be available at:
```
http://127.0.0.1:8000/docs
```

## Documentation
The documentation `/docs/openapi.yml` 

You can catch up this app (with demo database) online at:

https://ikd2xw.deta.dev/docs#/


username: `admin`
password: `admin`


Also, when you start the project locally  `http://127.0.0.1:8000/docs/`.


## Contact the author
>[LinkedIn](http://linkedin.com/in/maxim-usanin/)

>[Telegram](https://t.me/m5286606)

>[Portfolio](https://github.com/diplodoc13)