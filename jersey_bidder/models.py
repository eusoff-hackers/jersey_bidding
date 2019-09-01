from flask import current_app
from jersey_bidder import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model):
    __table_args__ = {'extend_existing': True}   
    roomNumber = db.Column(db.String(20), primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(5), nullable=False)

    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    #foreign key constraint
    choice = db.relationship('Choice', backref='user', lazy=True)

class Choice(db.Model):
    __table_args__ = {'extend_existing': True}     
    id = db.Column(db.Integer, primary_key=True)
    submitDatetime = db.Column(db.DateTime, nullable=False)
    firstChoice = db.Column(db.Integer, nullable=False)
    secondChoice = db.Column(db.Integer, nullable=False)
    thirdChoice = db.Column(db.Integer, nullable=False)
    fourthChoice = db.Column(db.Integer, nullable=False)
    fifthChoice = db.Column(db.Integer, nullable=False)

    #foreign key constraint
    roomNumber = db.Column(db.String(20), db.ForeignKey('user.roomNumber'))
    
#To do in documentation! initialize/changing databse models:
"""
1. python3 
2. from jersey_bidder import create_app, db
3. create an app: app = create_app()
4. run:
    with app.app_context():
        db.create_all()
5. this creates a new relation in the specified DB 
6. quit() to leave the python3 interpreter
"""

    

    
