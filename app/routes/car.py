from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from app.models.car import Car
from app.models.owner import Owner
from app import db

car_bp = Blueprint('car_management', __name__, url_prefix='/cars')

@car_bp.route('/', methods=['GET'])
def retrieve_all_cars():
    try:
        all_cars = Car.query.all()
        return jsonify({'cars': [car.to_dict() for car in all_cars]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@car_bp.route('/', methods=['POST'])
def create_car():
    request_data = request.get_json()
    owner_id = request_data.get('owner_id')
    if not owner_id:
        return jsonify({'error': 'owner_id is required'}), 400
    
    owner = db.session.query(Owner).get(owner_id)
    if not owner:
        return jsonify({'error': f'Owner with id {owner_id} not found'}), 404
    if len(owner.cars) >= 3:
        return jsonify({'error': f'Owner {owner.name} already has the maximum number of cars (3)'}), 400

    model = request_data.get('model')
    color = request_data.get('color')
    if model not in ['sedan', 'hatch', 'convertible']:
        return jsonify({'error': f'{model} is not a valid car model'}), 400
    if color not in ['gray', 'blue', 'yellow']:
        return jsonify({'error': f'{color} is not a valid car color'}), 400

    new_car = Car(color=color, model=model)
    owner.cars.append(new_car)
    db.session.add(new_car)
    db.session.commit()
    return jsonify({'car': new_car.to_dict()}), 201

@car_bp.route('/<int:car_id>', methods=['GET'])
def retrieve_car(car_id):
    car = db.session.get(Car, car_id)
    if not car:
        return jsonify({'error': f'Car with id {car_id} not found'}), 404
    return jsonify({'car': car.to_dict()})

@car_bp.route('/<int:car_id>', methods=['PUT'])
def modify_car(car_id):
    car = db.session.get(Car, car_id)
    if not car:
        return jsonify({'error': f'Car with id {car_id} not found'}), 404

    request_data = request.get_json()
    color = request_data.get('color')
    model = request_data.get('model')
    
    if color:
        car.color = color
    if model:
        car.model = model
    
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Could not update car'}), 500

    return jsonify({'car': car.to_dict()})

@car_bp.route('/<int:car_id>', methods=['DELETE'])
def remove_car(car_id):
    car = db.session.get(Car, car_id)
    if not car:
        return jsonify({'error': f'Car with id {car_id} not found'}), 404

    db.session.delete(car)
    db.session.commit()
    return '', 204
