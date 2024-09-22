def test_register_user(test_client):
    client, token = test_client
    json_data = {
        'username': 'lucas',
        'password': '@senhateste123'
    }
    response = client.post(f'api/auth/register', json=json_data)
    assert response.status_code == 201
    assert response.json['message'] == 'User created successfully'

def test_login_user(test_client):
    client, token = test_client
    json_data = {
        'username': 'lucas',
        'password': '@senhateste123'
    }
    response = client.post(f'api/auth/login', json=json_data)
    assert response.status_code == 200
    assert 'access_token' in response.get_json()