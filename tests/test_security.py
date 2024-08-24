from jwt import decode
from http import HTTPStatus
from fast_zero.security import SECRET_KEY, create_acess_token


def test_jwt():
    data = {'test': 'test'}
    token = create_acess_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp']  # testa se o valor de exp foi adicionado ao toked
    
    
def test_jwt_invalid_token(client):
    response = client.delete(
        ...'/users/'=
    )