from application import application
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(application)

class Bank_Details(db.Model):
    __tablename__ = 'bank_details'
    ifsc = db.Column('ifsc', db.String, nullable=False, primary_key=True)
    bank_id = db.Column('bank_id', db.Integer)
    branch = db.Column('branch', db.String)
    address = db.Column('address', db.String)
    city = db.Column('city', db.String)
    district = db.Column('district', db.String)
    state = db.Column('state', db.String)
    bank_name = db.Column('bank_name', db.String)
