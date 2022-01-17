## API development course
Develop and deploy backend for a forum using python FastAPI and other tools. Based on [this course](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=2005s&ab_channel=freeCodeCamp.org).

## Environment
Conda env
```sh
conda create -n fastapi python=3.9
conda activate fastapi
pip install uvicorn fastapi[all] sqlalchemy psycopg2 passlib[bcrypt] python-jose[cryptography] alembic # our stack
# or pip install -r requirements.txt
```

In addition, PostgreSQL is the database of choice for the project. Other useful but optional debugging tools are pgAdmin and Postman.

`.env` file with DB credentials and JWT settings is not included:
```txt
    DB_HOSTNAME=
    DB_PORT=
    DB_PASSWORD=
    DB_NAME=
    DB_USERNAME=
    JWT_SECRET_KEY=
    JWT_ALGORITHM=
    JWT_TOKEN_EXPIRE_MINUTES=
```

_Note: JWT key can begenerated using `openssl rand -hex 32` command_.
## Start

Dev environment servers start using `uvicorn` library

```sh
uvicorn app.main:app --reload --port 8080
```

## API Docs
```
localhost:8000/docs
```

## Alembic (DB migration)
Create revision with update and downgtrade logic
```sh
alembic revision -m 'add content column'
```

To update to a given revision, downgrade 1 step back
```sh
alembic upgrade <rev_number> # or heads to upgrade to latest
alembic downgrade -1
```

View latest and current revision 
```sh
alembic heads
alembic current
```

Auto generate features to match the established sqlalchemy models. Can be used to quick start a db from sql models, or to update the db if you change sql models, so that the DB always follows the code.
```sh
alembic revision --autogenerate -m "autocomplete my schemas"
```
        