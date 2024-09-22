from app import db

class Car(db.Model):
    __tablename__ = "cars"

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.Enum("convertible", "hatch", "sedan"), nullable=False)
    color = db.Column(db.Enum("blue", "yellow", "gray"), nullable=False)
    owner = db.relationship("Owner", backref=db.backref("cars", lazy=True))
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.id"), nullable=False)

    def __repr__(self):
        return f"<Car(color={self.color}, model={self.model})>"

    def to_dict(self):
        return {
            'id': self.id,
            'model': self.model,
            'color': self.color
        }
