from . import db,login_manager
from datetime import datetime
from flask_login import UserMixin
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(length=30), nullable=False)
    email=db.Column(db.String(length=50), nullable=False, unique=True)
    password=db.Column(db.String(length=60), nullable=False)
    notes=db.relationship('Notes')

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data=db.Column(db.String(length=3000), nullable=False)
    date=db.Column(db.DateTime(), default=datetime.utcnow())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))



