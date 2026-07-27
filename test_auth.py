from app.tests.conftest import client


def test_register_and_login():
    response = client.post('/api/auth/register', json={
        'name': 'Test Student',
        'email': 'student@example.com',
        'password': 'strongpassword',
    })
    assert response.status_code == 200
    assert response.json()['email'] == 'student@example.com'

    login_response = client.post('/api/auth/login', json={
        'email': 'student@example.com',
        'password': 'strongpassword',
    })
    assert login_response.status_code == 200
    body = login_response.json()
    assert 'access_token' in body
    assert body['token_type'] == 'bearer'


def test_invalid_login():
    response = client.post('/api/auth/login', json={'email': 'bad@example.com', 'password': 'wrong'})
    assert response.status_code == 401
