from . import db  # The dot basically means "Website"
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
import pytz

def GetTime():
    TP_time = datetime.now(pytz.timezone('Asia/Taipei'))
    return TP_time

Current_Time = GetTime


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=Current_Time)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # ('user.id') above is from the User class below except lower case (SQL foreigen key rule)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    user_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    # ('Note') is not lower case because it's a relationship and not foreign key
