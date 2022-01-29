from src.cognito import Cognito
import pytest

def test_cognito_init():
    with pytest.raises(ValueError):
        Cognito(87)

@pytest.mark.parametrize('email, id',[
    ('somemail@example.com','9103'),
    ('another@email.com', '2pukgsua3nloh6m1ctrtu995cs')
])
def test_create_user(email, id):
    with pytest.raises(Exception):
        c = Cognito(email)
        c.create_user(id)