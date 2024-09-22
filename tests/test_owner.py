import pytest
from app.models.owner import Owner
from app import db

def generate_auth_headers(token):
    return {'Authorization': f'Bearer {token}'}

@pytest.mark.parametrize("owner_id, expected_name", [
    (1, 'Lucas Morais')
])
def test_retrieve_owner(test_client, owner_id, expected_name):
    client, token = test_client
    auth_headers = generate_auth_headers(token)
    response = client.get(f'/api/owners/{owner_id}', headers=auth_headers)

    assert response.status_code == 200
    assert response.json['name'] == expected_name

def test_create_owner(test_client):
    client, token = test_client
    new_owner_data = {'name': 'Lucas addOwner'}
    auth_headers = generate_auth_headers(token)
    response = client.post('/api/owners', headers=auth_headers, json=new_owner_data, follow_redirects=True)

    assert response.status_code == 201
    assert response.json['name'] == new_owner_data['name']

def test_update_existing_owner(test_client):
    client, token = test_client
    updated_owner_data = {'name': 'Lucas UpdateOwner'}
    auth_headers = generate_auth_headers(token)
    response = client.put('/api/owners/1', headers=auth_headers, json=updated_owner_data)

    assert response.status_code == 200
    assert response.json['name'] == updated_owner_data['name']

def test_remove_owner(test_client):
    client, token = test_client
    auth_headers = generate_auth_headers(token)
    response = client.delete('/api/owners/1', headers=auth_headers)

    assert response.status_code == 204
    assert db.session.get(Owner, 1) is None
