from project.app import db
from flask_login import UserMixin
from datetime import datetime

class Users(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String,nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.timezone.utc)

    #digunkan untuk mencetak string setiap kali membuat elemen baru
    def __repr__(self):
        return '<Users %r>' % self.id
    