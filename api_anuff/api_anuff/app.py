from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    return {'message': 'Olá mundo!'}

@app.post('/usuarios/', status_code=HTTPStatus.CREATED)
def criar_usuario():
    pass