# Proof of concept for fastapi
The project is developed for the Python Level Up course.

## Used technologies
* Python 3.8
* fastapi
* uvicorn
* pytest
* postgres
* docker-compose

## Run app

Download source and requiremets.txt and in the terminal type in the root directory:

* basic

`uvicorn views.main:app`

* auto-reload:

`uvicorn views.main:app --reload`

## Cloud

Api is available on heroku cloud:

https://py-lvl-up-1.herokuapp.com/

API docs:

https://py-lvl-up-1.herokuapp.com/docs

## Notes
###to run type:
`docker-compose up`

###run with postgres [Linux]:
`SQLALCHEMY_DATABASE_URL="postgresql://postgres:DaftAcademy@127.0.0.1:5555/postgres" uvicorn views.main:app --reload --host=0.0.0.0 --port=${PORT:-5000}`

###run with postgres [Win10] with venv (e.g. PyCharm)
`set SQLALCHEMY_DATABASE_URL=postgresql://postgres:DaftAcademy@127.0.0.1:5555/postgres`

`uvicorn views.main:app --reload`


###pytest

* to run all tests type in terminal:  
`pytest`
*  to run custom method by fragment of name:  
`pytest -svk employee`

###connecting to DB locally:
1) run a docker
2) `docker-compose up`
3) `docker-compose exec postgres bash`
3) `psql -U postgres`
5) `select * ....`
6) to see tables: `\dt`  to exit: `\q`

###DB migration:
1) connect to docker
2) `psql -U postgres < docker-entrypoint-initdb.d/migration.sql`

###send a dump to heroku [RAW FILE !!! not preview]:
`heroku pg:backups:restore https://github.com/mateusz91t/PyLvlUp1/raw/master/migrations/northwind.dump --app py-lvl-up-1 --confirm py-lvl-up-1`
