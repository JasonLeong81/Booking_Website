import os
import psycopg2

DATABASE_URL = 'postgres://roxkgnqetyxixw:67ca597f8a78b5ee8d03c73d4620eda63d077ba926b908e87e674ae9756aa838@ec2-52-213-167-210.eu-west-1.compute.amazonaws.com:5432/dfo78uaep5lbi8' # from https://medium.com/analytics-vidhya/heroku-deploy-your-flask-app-with-a-database-online-d19274a7a74'

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
# conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
r = cur.execute("""select 'User.id' from User;""")
results = r.fetchall()
for i in results:
    print(i)
