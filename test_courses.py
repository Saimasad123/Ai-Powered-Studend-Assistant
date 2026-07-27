from app.tests.conftest import client


def test_course_crud():
    client.post('/api/auth/register', json={
        'name': 'Course Student',
        'email': 'course@example.com',
        'password': 'password123',
    })
    token = client.post('/api/auth/login', json={'email': 'course@example.com', 'password': 'password123'}).json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    create_resp = client.post('/api/courses', json={'course_name': 'Database Systems', 'course_code': 'CSC204', 'description': 'Test course'}, headers=headers)
    assert create_resp.status_code == 200
    course = create_resp.json()
    assert course['course_name'] == 'Database Systems'

    list_resp = client.get('/api/courses', headers=headers)
    assert list_resp.status_code == 200
    assert any(item['course_name'] == 'Database Systems' for item in list_resp.json())

    update_resp = client.put(f"/api/courses/{course['id']}", json={'course_name': 'DB Systems', 'course_code': 'CSC204', 'description': 'Updated'}, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()['course_name'] == 'DB Systems'

    delete_resp = client.delete(f"/api/courses/{course['id']}", headers=headers)
    assert delete_resp.status_code == 200
    assert delete_resp.json()['detail'] == 'Course deleted'
