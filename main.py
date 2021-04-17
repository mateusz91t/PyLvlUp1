from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def root_view():
    return {'message': "Hello"}


@app.get("/hello/{name}")
def hello_name_view(name: str):
    return f"Hello {name}"

# to run type:
# uvicorn main:app
