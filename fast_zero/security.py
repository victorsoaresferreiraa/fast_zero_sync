from datetime import datetime, timedelta

from jwt import encode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = PasswordHash.recommended()

def create_acess_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTF')) + timedelta(
        minutes=ACESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    enconded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return enconded_jwt