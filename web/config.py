import os
class Config:
    SECRET_KEY = 'jason'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///jason.db'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI ='postgres://ffssqvauahbwit:abfcd75994bb9fcebb8cac1eb5c9b7078d82929c6a5245b0500e6c22b6d06223@ec2-34-254-69-72.eu-west-1.compute.amazonaws.com:5432/d8959l3lb2bqep'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'leongjason822@gmail.com'
    MAIL_PASSWORD = '378100Yc'


