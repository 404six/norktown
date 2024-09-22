from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        """set the password for the user, hashing it before storing"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """check if the provided password matches the stored hashed password"""
        return check_password_hash(self.password_hash, password)
