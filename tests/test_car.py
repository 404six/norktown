from app.models.car import Car
from app import db

def generate_auth_headers(token):
    return {'Authorization': f'Bearer {token}'}

def test_retrieve_cars_by_owner_id(test_client):
    client, token = test_client
    response = client.get('/api/cars/1', headers=generate_auth_headers(token))
    assert response.status_code == 200

def test_create_car(test_client):
    client, token = test_client
    car_data = {'owner_id': 1, 'color': 'yellow', 'model': 'convertible'}
    response = client.post('/api/cars', json=car_data, headers=generate_auth_headers(token), follow_redirects=True)
    
    assert response.status_code == 201
    assert response.json['car']['color'] == car_data['color']
    assert response.json['car']['model'] == car_data['model']

def test_update_existing_car(test_client):
    client, token = test_client
    updated_data = {'model': 'sedan', 'color': 'blue'}
    response = client.put('/api/cars/1', json=updated_data, headers=generate_auth_headers(token))

    assert response.status_code == 200
    assert response.json['car']['model'] == updated_data['model']
    assert response.json['car']['color'] == updated_data['color']

def test_add_car_exceeds_owner_limit(test_client):
    client, token = test_client
    excess_car_data = {'owner_id': 1, 'model': 'hatch', 'color': 'yellow'}
    response = client.post('/api/cars', json=excess_car_data, headers=generate_auth_headers(token), follow_redirects=True)

    assert response.status_code == 400
    assert 'error' in response.json

def test_create_car_with_invalid_data(test_client):
    client, token = test_client
    invalid_car_data = {'owner_id': 1, 'color': 'test_color', 'model': 'test_model'}
    response = client.post('/api/cars', json=invalid_car_data, headers=generate_auth_headers(token), follow_redirects=True)

    assert response.status_code == 400

def test_remove_car(test_client):
    client, token = test_client
    response = client.delete('/api/cars/1', headers=generate_auth_headers(token))

    assert response.status_code == 204
    assert db.session.get(Car, 1) is None
