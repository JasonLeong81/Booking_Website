import os
import psycopg2 # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries


class Config:
    SECRET_KEY = 'jason'
    SQLALCHEMY_DATABASE_URI = 'postgres://ohdamdgyjdijjh:490b92ceb79119226d9a813d2a0fca176c0abef6f3af90be03bd7ed6dfaa7dd2@ec2-34-255-134-200.eu-west-1.compute.amazonaws.com:5432/d3ii73kejc58fe'
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


