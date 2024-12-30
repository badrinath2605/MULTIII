from . import badridb
from sqlalchemy import Column, Integer, String,func
from flask_login import UserMixin

class User(badridb.Model,UserMixin):
    id=badridb.Column(badridb.Integer,primary_key=True)
    email=badridb.Column(badridb.String(150),unique=True)
    password=badridb.Column(badridb.String(150))
    username=badridb.Column(badridb.String(150))
    full_name=badridb.Column(badridb.String(150))
    profile_photo=badridb.Column(badridb.String(150))
    dob=badridb.Column(badridb.String(10))
    yearOfStudy=badridb.Column(badridb.String(5))
    mobilenumber=badridb.Column(badridb.String(15))
    notes=badridb.relationship('Note')#everytime user adds a note it gets added here
class Note(badridb.Model):
    id=badridb.Column(badridb.Integer,primary_key=True)
    file_name=badridb.Column(badridb.String(50))
    data=badridb.Column(badridb.String(10000))
    floder=badridb.Column(badridb.String(20))
    date=badridb.Column(badridb.DateTime(timezone=True), default=func.now())
    user_id=badridb.Column(badridb.Integer,badridb.ForeignKey('user.id'))
    filedata=badridb.Column(badridb.LargeBinary)

#class pdf(badridb.Model):
