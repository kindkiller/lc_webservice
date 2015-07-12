# -*- coding: utf-8 -*-
import sys
from sqlalchemy import Table, ForeignKey
from sqlalchemy import *
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
#import pytz
import mysql.connector
from sqlalchemy import create_engine

db_uri = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}"
#engine = create_engine(db_uri.format(user='allen', password='yao0702', host='192.168.1.103', port='3306', db='userdb'), encoding='utf8', connect_args={'time_zone':'+00:00'})
engine = create_engine(db_uri.format(user='yy', password='qwer4321', host='localhost', port='3306', db='userdb'), encoding='utf8', connect_args={'time_zone':'+00:00'})#
# engine = create_engine('sqlite:///feed.db', echo=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
sess = Session()

'''class BaseModel(Base):
    __tablename__ = 'basemodel'
    class Meta:
        abstract = True
'''

class Userinfo(Base):
    __tablename__='userinfo'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String, primary_key=True, default="")
    Email = Column(String, primary_key=True, default="")
    Password = Column(String(50))
    Salt = Column(VARBINARY(50))
    Active = Column(Integer)
    LastLoginTime = Column(DateTime)


def AddNewUser(Username, Pword):
    from datetime import datetime
    newUser=Userinfo(Username=Username, Password=Pword,Active=1, LastLoginTime=datetime.utcnow())
    try:
        sess.add(newUser)
        sess.commit()
    except:
        print ('Unexpect Exception:', sys.exc_info()[0])
        sess.rollback()
        return False
    return True

def CheckUser(Username, Pword):
    user=sess.query(Userinfo).filter(Userinfo.Username==Username).all()
    if len(user)>0:
        if (Pword==user[0].Password):
            return True
        else:
            return False
    else:
        return False
    return False

class Userdetails(Base):

    __tablename__='userdetails'
    ID=Column(Integer, primary_key=True, autoincrement=True)
    UserID=Column(Integer,ForeignKey('userinfo.ID'))
    AliasName=Column(String(50))
    Country=Column(String(50))
    About_me=Column(String(150))
    AgeRange=Column(Integer,ForeignKey('AgeRange.ID'))
    InterestArea=Column(Integer,ForeignKey('InterestArea.ID'))
    Update_Date=Column(DateTime)


def AddUserDetail(UserId,UserNickName,Country,Aboutme,Age,InterestArea):
     from datetime import datetime
     ageRange=sess.query(AgeRange).filter(AgeRange.AgeRangeStart<Age and AgeRange.AgeRangeEnd<Age)
     detail=Userdetails(UserID=UserId,AliasName=UserNickName,Country=Country,About_me=Aboutme,Agerange=ageRange[0].ID,InterestArea=InterestArea,Update_Date=datetime.utcnow())
     try:
         sess.add(detail)
         sess.commit()
     except:
         print ("Unexpect Exception:", sys.exc_info()[0])
         sess.rollback()
         return False
     return True


class AgeRange(Base):

    __tablename__='agerange'
    ID= Column(Integer, primary_key=True, autoincrement=True)
    AgeRangeStart= Column(Integer)
    AgeRangeEnd=Column(Integer)


class Tags(Base):

    __tablename__='tags'
    ID=Column(Integer,primary_key=True, autoincrement=True)
    TagName=Column(String)
    Tag_Text=Column(String)
    latitude=Column(String)
    longitude=Column(String)
    TAddDate=Column(DateTime)


class InterestArea(Base):

    __tablename__='interestarea'
    ID=Column(Integer,primary_key=True, autoincrement=True)
    Name=Column(String)
    Description=(String)

class RelationType(Base):

    __tablename__='relationtype'
    ID=Column(Integer,primary_key=True, autoincrement=True)
    RelationType=Column(String)

class PropertyType(Base):

    __tablename__='propertytype'
    PropertyTypeID=Column(Integer,primary_key=True, autoincrement=True)
    Name=Column(String)
    DataType=Column(String)

class PhotoInfo(Base):

    __tablename__='photoinfo'
    PhotoID=Column(Integer,primary_key=True)
    PhotoProperty=Column(Integer,ForeignKey('PropertyType.PropertyTypeID'))
    Value=Column(String)

class Photos(Base):
    __tablename__='photos'
    ID=Column(Integer,primary_key=True, autoincrement=True)
    Name=Column(String)
    Description=Column(String)
    Path=Column(String)
    Filename=Column(String)
    PAddDate=Column(DateTime)

    #UserID=Column(Integer,ForeignKey('UserInfo.ID'))

class PhotoTag(Base):

    __tablename__='PhotoTag'
    PhotoID=Column(Integer,primary_key=True)
    TagId=Column(Integer,primary_key=True)

class Likes(Base):

    __tablename__='likes'
    ID=Column(Integer,primary_key=True, autoincrement=True)
    UserID=Column(Integer, ForeignKey('userInfo.ID'))
    PhotoID=Column(Integer,ForeignKey('photos.ID'))

class Comments(Base):

    __tablename__='comments'
    ID=Column(Integer, primary_key=True, autoincrement=True)
    Context=Column(String)
    UserID=Column(Integer,ForeignKey('UserInfo.ID'))
    PhotoID=Column(Integer,ForeignKey('Photos.ID'))
    AddDate=Column(DateTime)

class ProfilePhoto(Base):
    __tablename__='profilephoto'
    UserID=Column(Integer,ForeignKey('userInfo.ID'),primary_key=True)
    PhotoID=Column(Integer,ForeignKey('photos.ID'),primary_key=True)

class UserRelation(Base):
    __tablename__='userrelation'
    #Actor
    User1ID=Column(Integer,ForeignKey('userinfo.ID'),primary_key=True)
    #Target
    User2ID=Column(Integer, ForeignKey('userinfo.ID'),primary_key=True)
    #RelationType
    Type=Column(Integer,ForeignKey('relationtype.ID'))



a=sess.query(Photos).all()
output="PhotoID:{ID}; Description:{Description}"
print (output.format(ID=a[0].ID, Description=a[0].Description))
user = sess.query(Userinfo).filter(Userinfo.Email =='yao@yao.com')
for u in user:
    print (u.Password)
#
# if CheckUser('LD','120'):
#     print 'logined'
# else:
#     print 'wrong'
#
# if CheckUser('LD','000'):
#     print 'Login'
# else:
#     print 'wrong'
#
#
# class User(Base):
#
#     __tablename__ = 'user'
#     id=Column(Integer, primary_key=True)
#     password = Column(String)
#
#
# class Item(Base):
#     __tablename__ = 'item'
#     id=Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     image = Column(String)
#     source_url = Column(String)
#     message = Column(String)
#     pin_count = Column(Integer, default=0)
#
#
#     '''
#     user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     image = models.ImageField(upload_to='items')
#     source_url = models.TextField()
#     message = models.TextField(blank=True, null=True)
#     pin_count = models.IntegerField(default=0)
# '''
#     # class Meta:
#     #    db_table = 'pinterest_example_item'
#
#
# class Board(Base):
#
#     __tablename__ = 'board'
#     id=Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     name = Column(String)
#     description = Column(String)
#     slug = Column(String)
# '''
#     user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     slug = models.SlugField()
# '''
#
#
# class Pin(Base):
#
#     __tablename__ = 'pin'
#     id=Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     item_id = Column(Integer, ForeignKey('item.id'))
#     board_id = Column(Integer, ForeignKey('board.id'))
#     message = Column(String)
#     created_at = Column(DateTime, default=func.now())
#
#
#     def create_activity(self):
#         from stream_framework.activity import Activity
#         from verbs import Pin as PinVerb
#         activity = Activity(
#             self.user_id,
#             PinVerb,
#             self.id,
#             self.influencer_id,
#             time=self.created_at,
#             #time=make_naive(self.created_at, pytz.utc),
#             extra_context=dict(item_id=self.item_id)
#         )
#         return activity
# '''
#     user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     item = models.ForeignKey(Item)
#     board = models.ForeignKey(Board)
#     influencer = models.ForeignKey(
#         settings.AUTH_USER_MODEL, related_name='influenced_pins')
#     message = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
# '''
#
#
# class Follow(Base):
#
#     '''
#     A simple table mapping who a user is following.
#     For example, if user is Kyle and Kyle is following Alex,
#     the target would be Alex.
#     '''
#
#
#     __tablename__ = 'Follow'
#     id=Column(Integer, primary_key=True)
#     user = Column(Integer, ForeignKey('user.id'))
#     target = Column(Integer, ForeignKey('user.id'))
#     created_at = Column(DateTime, default=func.now())
#
#
# '''
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, related_name='following_set')
#     target = models.ForeignKey(
#         settings.AUTH_USER_MODEL, related_name='follower_set')
#     created_at = models.DateTimeField(auto_now_add=True)
# '''
#
# stmt = text("""select *
#                from test_usertable
#                where username=:username""")
#             # s is instance of Session() class factory
# #results = sess.execute(stmt, params=dict(username=username))
#
#
#
# cnx = mysql.connector.connect(user="allen",password="yao0702",host="192.168.1.103",database="userdb")
# cursor = cnx.cursor()
# cursor.callproc("uspTest_usertable",args=("allen5","allenTest"))
# #cursor.execute("select * from test_usertable")
# #cursor.fetchall()
# cnx.commit()
#
# #results = exec_procedure(sess,"uspTest_usertable",['allen2','allenpw'], **t)
# #results = exec
#
# #sess.execute("select * from test_usertable")
# #Base.metadata.create_all(engine)
#
