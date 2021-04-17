from fastapi import FastAPI

from myserives.methods_for_main import count

app = FastAPI()
app.counter = count()

# to run type:
# uvicorn main:app


@app.get('/')
def root_view():
    return {'message': "Hello"}


@app.get("/hello/{name}")
def hello_name_view(name: str):
    return f"Hello {name}"


@app.get("/counter")
def counter_viev():
    return next(app.counter)
