import pytest
from app import create_app, db
from app.models.car import Car
from app.models.owner import Owner
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')
    testing_client = flask_app.test_client()

    with flask_app.app_context():
        db.create_all()
        owner_id = initialize_test_data()

        test_token = create_access_token(identity=owner_id)

        yield testing_client, test_token

        db.session.remove()
        db.drop_all()

def initialize_test_data():
    test_owner = Owner(name='Lucas Morais')
    db.session.add(test_owner)
    db.session.commit()

    test_cars = [
        Car(model='convertible', color='yellow', owner_id=test_owner.id),
        Car(model='hatch', color='blue', owner_id=test_owner.id),
    ]
    db.session.bulk_save_objects(test_cars)
    db.session.commit()

    return test_owner.id
