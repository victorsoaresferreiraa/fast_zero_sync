from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPSException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import TokenData

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credential_exception = HTTPSException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},

    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')

        if not username:
            raise credential_exception
        token_data = TokenData(username=username)

    except DecodeError:
        raise credential_exception

    user = session.scalar(
        select(User).where(User.email) == token_data.username
        )

    if not user:
        raise credential_exception

    return user


def create_acess_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTF')) + timedelta(
        minutes=ACESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    enconded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return enconded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)
    print(get_password_hash)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
