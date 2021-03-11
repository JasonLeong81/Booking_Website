import os
class Config:
    SECRET_KEY = 'jason'

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///jason.db' # for deployment
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'  # for testing

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI ='postgres://ysrqfbbqcroxrk:7836ec49050c77b20c5ef5a7ae20afd3ca6995113083ee5a8de647af65218915@ec2-54-74-14-109.eu-west-1.compute.amazonaws.com:5432/dfbp68fivhnfte'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'leongjason822@gmail.com'
    MAIL_PASSWORD = '378100Yc'


# no module names psycopg2 -> pip install psycopg2


### Accounts ###
# xxx@gmail.com
# x@gmail.com
# admin: admin@gmail.com