from app import app, db


class User(db.Model):
    __tablename__ = 'user'

    username = db.Column(db.String, primary_key=True)
    college_code = db.Column(db.String)

    registered_at = db.Column(db.Integer)
    last_seen = db.Column(db.Integer)
