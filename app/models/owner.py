from app import db

class Owner(db.Model):
    __tablename__ = "owners"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    is_car_owner = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Owner(name={self.name})>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_car_owner': self.is_car_owner
        }
