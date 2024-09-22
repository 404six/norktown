from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required
from app import db
from app.models.owner import Owner
from app.models.car import Car

owner_bp = Blueprint("owner_management", __name__, url_prefix="/owners")

@owner_bp.before_request
@jwt_required()
def check_jwt_token():
    pass

def extract_owner_name(request_data):
    owner_name = request_data.get("name")
    if not owner_name:
        return jsonify({"error": "Missing name parameter"}), 400
    return owner_name

@owner_bp.route("/", methods=["POST"])
def add_owner():
    request_data = request.json
    owner_name = extract_owner_name(request_data)
    if isinstance(owner_name, tuple):
        return owner_name

    new_owner = Owner(name=owner_name)
    db.session.add(new_owner)
    db.session.commit()
    return jsonify({"owner_id": new_owner.id, "name": new_owner.name}), 201

@owner_bp.route("/<int:owner_id>", methods=["PUT"])
def modify_owner(owner_id):
    existing_owner = db.session.get(Owner, owner_id)
    if existing_owner is None:
        abort(404)

    request_data = request.json
    owner_name = extract_owner_name(request_data)
    if isinstance(owner_name, tuple):
        return owner_name

    existing_owner.name = owner_name
    db.session.commit()
    return jsonify({"owner_id": existing_owner.id, "name": existing_owner.name}), 200

@owner_bp.route("/", methods=["GET"])
def list_all_owners():
    all_owners = Owner.query.all()
    response = [{"owner_id": owner.id, "name": owner.name, "is_car_owner": owner.is_car_owner} for owner in all_owners]
    return jsonify(response), 200

@owner_bp.route("/<int:owner_id>", methods=["GET"])
def retrieve_owner(owner_id):
    specific_owner = Owner.query.get_or_404(owner_id)
    return jsonify({"owner_id": specific_owner.id, "name": specific_owner.name, "is_car_owner": specific_owner.is_car_owner}), 200

@owner_bp.route("/<int:owner_id>", methods=["DELETE"])
def remove_owner(owner_id):
    owner_to_delete = Owner.query.get_or_404(owner_id)
    associated_cars = Car.query.filter_by(owner_id=owner_to_delete.id).all()

    for car in associated_cars:
        db.session.delete(car)

    db.session.delete(owner_to_delete)
    db.session.commit()

    return jsonify({'message': f'Owner with id {owner_id} has been deleted'}), 204
