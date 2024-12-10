from http import HTTPStatus

from fastapi import FastAPI

from api_anuff.api_anuff.schemas import Message, UsuarioBase, UsuarioRead

app = FastAPI()

database = []

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}

@app.post('/usuarios/', status_code=HTTPStatus.CREATED, response_model=UsuarioRead)
def criar_usuario(usuario: UsuarioBase):
    return usuario

@app.post