import os
import psycopg2


class Config:
    SECRET_KEY = 'jason'
    SQLALCHEMY_DATABASE_URI = 'postgres://roxkgnqetyxixw:67ca597f8a78b5ee8d03c73d4620eda63d077ba926b908e87e674ae9756aa838@ec2-52-213-167-210.eu-west-1.compute.amazonaws.com:5432/dfo78uaep5lbi8' # from https://medium.com/analytics-vidhya/heroku-deploy-your-flask-app-with-a-database-online-d19274a7a749
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///jason.db' # for deployment
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'  # for testing

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI ='postgres://ysrqfbbqcroxrk:7836ec49050c77b20c5ef5a7ae20afd3ca6995113083ee5a8de647af65218915@ec2-54-74-14-109.eu-west-1.compute.amazonaws.com:5432/dfbp68fivhnfte'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'leongjason822@gmail.com'
    MAIL_PASSWORD = '378100Yc'
    STRIPE_PUBLIC_KEY = 'pk_test_51IUY9XGCE7nPsl2DMpG9KvaBhWxgIreDeG24Mqks7nAiBURMh03M0PbjkEIILDD4UOTapBV8SvTIda6DbGTOopcn00NFCuixYg'
    STRIPE_SECRET_KEY = 'sk_test_51IUY9XGCE7nPsl2DUPJnUkFAZSBBSxlOK68BRpbWv8EYFETJtlVbjpakbrd7YVPuUnx41kDMa28qKXzxiSbYJTnf00iV2vF3uH'

# no module names psycopg2 -> pip install psycopg2


### Accounts ###
# xxx@gmail.com
# x@gmail.com
# admin: admin@gmail.com