# Mostra o status do codigo
from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from sqlalchemy import Session, create_engine, select

from fast_zero.models import User
from fast_zero.schemas import Message, UserDB, Userlist, UserPublic, UserSchema
from fast_zero.settings import Settings

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


# Recebe dados, referente ao create
@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    # Criando uma engine
    engine = create_engine(Settings().DATABASE_URL)

    # Criando uma session
    with Session(engine) as session:
        # Existem alguem que tem o email cadastrado
        db_user = session.scalar(
            # Escalar retorna ou o tima escalar
            # ou none
            # Seleciona o usuario, onde
            select(User).where(
                (User.username == user.username) | (User.email == user.email)
            )
        )

        if db_user:
            if db_user.username == user.username:
                raise HTTPException(
                    status_code=HTTPException.BAD_REQUEST,
                    detail='Username already existis',
                )
            elif db_user.email == user.email:
                raise HTTPException(
                    status_code=HTTPException.BAD_REQUEST,
                    detail='email already existis',
                )

        db_user = User(
            username=user.username, email=user.email, password=user.password
        )

        session.add(user)
        session.commit()
        session.refresh(db_user)

    return db_user()

    # Usando o debug do python
    # breakpoint()

    # usa nosso banco de dados falso, criando um registro
    # indo de 1 ate o tamanho final
    # user_with_id = UserDB(
    # Desempacotamento nomeado, passando para o USERBD as coisas
    # como username com o nome que esta no registro
    # Exemplo {'username': victor,
    # 'email': victorsoaresferreira09@gmail.com}
    #    **user.model_dump(),
    #    id=len(database) + 1,

    # Adicionando no nosso banco de dados, incrementando eles
    # database.append(user_with_id)

    # return user_with_id


@app.get('/users/', response_model=Userlist)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}
