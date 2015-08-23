__author__ = 'zoe'


import mysql.connector
from sqlalchemy import create_engine, true
from sqlalchemy.ext.declarative import declarative_base
from mysql.connector import MySQLConnection, Error

db_uri = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}"
userDB_engine = create_engine(db_uri.format(user='allen', password='yao0702', host='localhost', port='3306', db='userdb'),
                       encoding='utf8', connect_args={'time_zone': '+00:00'}, pool_size=100, pool_recycle=1800)

productDB_engine=create_engine(db_uri.format(user='allen', password='yao0702', host='localhost', port='3306', db='productdb'),
                       encoding='utf8', connect_args={'time_zone': '+00:00'}, pool_size=100, pool_recycle=1800)
# engine=create_engine(db_uri.format(user='yy', password='qwer4321', host='localhost', port='3306', db='userdb'), encoding='utf8', connect_args={'time_zone':'+00:00'})
# engine = create_engine('sqlite:///feed.db', echo=True)


# Used for enRichPictures, do not delete
Base = declarative_base()
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=userDB_engine)



conn = mysql.connector.connect(user="allen", password="yao0702", host="localhost", database="userdb")
conn.autocommit = true

productConn=mysql.connector.connect(user="allen", password="yao0702", host="localhost", database="productdb")
productConn.autocommit=true

# conn = mysql.connector.connect(user="yy",password="qwer4321",host="localhost",database="userdb")
# cursor = conn.cursor()
