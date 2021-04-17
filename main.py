from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def root():
    return {'message': "Hello"}

# to run type:
# uvicorn main:app