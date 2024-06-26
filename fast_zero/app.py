# Mostra o status do codigo
from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.schemas import Message, UserDB, Userlist, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


# Recebe dados, referente ao create
@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    # Usando o debug do python
    breakpoint()

    # usa nosso banco de dados falso, criando um registro
    # indo de 1 ate o tamanho final
    user_with_id = UserDB(
        id=len(database) + 1,
        # Desempacotamento nomeado, passando para o USERBD as coisas
        # como username com o nome que esta no registro
        # Exemplo {'username': victor,
        # 'email': victorsoaresferreira09@gmail.com}
        **user.model_dump(),
    )

    # Adicionando no nosso banco de dados, incrementando eles
    database.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=Userlist)
def read_users():
    return {'users': database}
