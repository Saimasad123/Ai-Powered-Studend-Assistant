import io
from app.tests.conftest import client


def test_document_upload_and_list():
    client.post('/api/auth/register', json={
        'name': 'Doc Student',
        'email': 'doc@example.com',
        'password': 'docpass123',
    })
    token = client.post('/api/auth/login', json={'email': 'doc@example.com', 'password': 'docpass123'}).json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    file_content = b'Introduction to Operating Systems\nDeadlock and scheduling.'
    files = {'files': ('lecture1.txt', io.BytesIO(file_content), 'text/plain')}
    response = client.post('/api/documents/upload', headers=headers, files=files)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]['original_filename'] == 'lecture1.txt'

    list_response = client.get('/api/documents', headers=headers)
    assert list_response.status_code == 200
    assert any(item['original_filename'] == 'lecture1.txt' for item in list_response.json())
