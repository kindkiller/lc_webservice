# -*- coding: utf-8 -*-
import sys
from sqlalchemy import Table, ForeignKey
from sqlalchemy import *
from sqlalchemy import Column, Integer, String, DateTime, func, FLOAT
from sqlalchemy.orm import relationship
import pytz
from mysql.connector import MySQLConnection, Error
from sys import exc_info
from datetime import datetime

from dbconnection import db_uri,userDB_engine, productDB_engine, Session, conn, productConn, Base

class Userinfo(Base):
    __tablename__ = 'userinfo'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String, primary_key=True, default="")
    Email = Column(String, primary_key=True, default="")
    Password = Column(String(50))
    Salt = Column(VARBINARY(50))
    Private_key=Column(String(255))
    Public_Key=Column(String(255))
    accessToken=Column(String(255))
    Active = Column(Integer)
    LastLoginTime = Column(DateTime)


class Userdetails(Base):
    __tablename__ = 'userdetails'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('userinfo.ID'))
    AliasName = Column(String(50))
    Country = Column(String(50))
    About_me = Column(String(150))
    AgeRange = Column(Integer, ForeignKey('AgeRange.ID'))
    InterestArea = Column(Integer, ForeignKey('InterestArea.ID'))
    Update_Date = Column(DateTime)
    Height=Column(Integer)
    Weight=Column(FLOAT)
    Brithday=Column(DateTime)
    Gender=Column(INTEGER)
    Occupation=Column(String(255))



class AgeRange(Base):
    __tablename__ = 'agerange'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    AgeRangeStart = Column(Integer)
    AgeRangeEnd = Column(Integer)


class Tags(Base):
    __tablename__ = 'tags'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    TagName = Column(String)
    Tag_Text = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    TAddDate = Column(DateTime)


class InterestArea(Base):
    __tablename__ = 'interestarea'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    Description = (String)


class RelationType(Base):
    __tablename__ = 'relationtype'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    RelationType = Column(String)


class PropertyType(Base):
    __tablename__ = 'propertytype'
    PropertyTypeID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    DataType = Column(String)


class PhotoInfo(Base):
    __tablename__ = 'photoinfo'
    PhotoID = Column(Integer, primary_key=True)
    PhotoProperty = Column(Integer, ForeignKey('PropertyType.PropertyTypeID'))
    Value = Column(String)


class Photos(Base):
    __tablename__ = 'photos'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    UID = Column(Integer)
    Name = Column(String)
    Description = Column(String)
    Path = Column(String)
    Filename = Column(String)
    PAddDate = Column(DateTime)

    def create_activity(self):
        from stream_framework.activity import Activity
        from verbs import Pin as PinVerb, AddPhoto
        activity = Activity(
            actor=self.UID,
            verb=AddPhoto,
            object=self.ID,
            # target=self.influencer_id,
            time=self.PAddDate,
            # time=make_naive(self.created_at, pytz.utc),
            extra_context=dict(item_id=self.ID)
        )

        return activity

        # UserID=Column(Integer,ForeignKey('UserInfo.ID'))


class PhotoTag(Base):
    __tablename__ = 'PhotoTag'
    PhotoID = Column(Integer, primary_key=True)
    TagId = Column(Integer, primary_key=True)


class Likes(Base):
    __tablename__ = 'likes'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('userInfo.ID'))
    PhotoID = Column(Integer, ForeignKey('photos.ID'))


class Comments(Base):
    __tablename__ = 'comments'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Context = Column(String)
    UserID = Column(Integer, ForeignKey('UserInfo.ID'))
    PhotoID = Column(Integer, ForeignKey('Photos.ID'))
    AddDate = Column(DateTime)


class ProfilePhoto(Base):
    __tablename__ = 'profilephoto'
    UserID = Column(Integer, ForeignKey('userInfo.ID'), primary_key=True)
    PhotoID = Column(Integer, ForeignKey('photos.ID'), primary_key=True)


class UserRelation(Base):
    __tablename__ = 'userrelation'
    # Actor
    User1ID = Column(Integer, ForeignKey('userinfo.ID'), primary_key=True)
    # Target
    User2ID = Column(Integer, ForeignKey('userinfo.ID'), primary_key=True)
    # RelationType
    Type = Column(Integer, ForeignKey('relationtype.ID'))


class Pin(Base):
    __tablename__ = 'pin'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('userinfo.id'))
    item_id = Column(Integer, ForeignKey('photos.id'))
    # board_id = Column(Integer, ForeignKey('board.id'))
    # influencer_id=Column(Integer,ForeignKey('userinfo.id'))
    message = Column(String)
    created_at = Column(DateTime, default=func.now())

    def create_activity(self):
        from stream_framework.activity import Activity
        from verbs import Pin as PinVerb
        activity = Activity(
            actor=self.user_id,
            verb=PinVerb,
            object=self.item_id,
            # target=self.influencer_id,
            time=self.created_at,
            # time=make_naive(self.created_at, pytz.utc),
            extra_context=dict(item_id=self.item_id)
        )

        return activity



#region: User Operation

def AddNewUser(Username, Pword, salt, email):
    from datetime import datetime
    try:
        cursor=conn.cursor()
        timeFormat='%Y-%m-%d %H:%M:%S'
        args = [Username,Pword, 0, salt, email, datetime.utcnow().strftime(timeFormat),0]
        result_args = cursor.callproc('uspAddUser', args)
        conn.commit()
        cursor.close()
        #print(result_args[6])
        return result_args[6]
    except Error as e:
        conn.rollback()
        cursor.close()
        print(e)
    return 0


def AddUserDetail(UserId, UserNickName, Country, Aboutme, Age, InterestArea,height,weight,isF,occupation):
    from datetime import datetime
    sess = Session()
    birthFormat='%Y-%m-%d'
    ageRange = sess.query(AgeRange).filter(AgeRange.AgeRangeStart < Age and AgeRange.AgeRangeEnd < Age)
    detail = Userdetails(UserID=UserId, AliasName=UserNickName, Country=Country, About_me=Aboutme,
                         Agerange=ageRange[0].ID, InterestArea=InterestArea, Update_Date=datetime.utcnow(),
                         Height=height, Weight=weight, Brithday=datetime.strftime(birthFormat),Gender=(isF),
                         Occupation=occupation)
    try:
        sess.add(detail)
        sess.commit()
    except:
        print "Unexpect Exception:", sys.exc_info()[0]
        sess.rollback()
        sess.close()
        return False
    sess.close()
    return True


def get_user_follower_ids_fromDB(uid):
    if uid == 0:
        return None
    cursor=conn.cursor()
    try:

        sql=("select user1ID from userrelation"
             " where User2ID=%(uid)s")
        data={"uid":uid}
        cursor.execute(sql,data)
        result=cursor.fetchall()
        if result is not None and len(result)>0:
            return result
    except:
        print (exc_info())
        return None
    finally:
        cursor.close()


def checkAvailableUsername(username):
    if (username is None):
        return False
    else:
        try:
            cursor=conn.cursor()
            sql="select username in userdb.userinfo where username =%(user)s "
            data={"user":username}
            cursor.execute(sql,data)
            if (cursor.rowcount>0):
                cursor.close()
                return False
            else:
                cursor.close()
                return True;
        except:
            print(exc_info())
            cursor.close()
            return False;

def CheckUser(Username, Pword):
    checksess = Session();
    user = checksess.query(Userinfo).filter(Userinfo.Username == Username).all()
    checksess.commit()
    checksess.close()

    if len(user) > 0:
        if (Pword == user[0].Password):
            return True
        else:
            return False
    else:
        return False
    return False

def getUserPasswordByID(userid):
    if userid<1:
        return None
    cursor=conn.cursor()
    try:
        sql="SELECT Password FROM userdb.userinfo WHERE ID =%(uid)s "
        data={"uid":userid}
        cursor.execute(sql,data)
        result=cursor.fetchall()
        if result is not None:
            cursor.close()
            return result[0][0]
        else:
            cursor.close()
            return None;
    except:
        print(exc_info())
        cursor.close()
        return None;

def getUserPasswordByName(username):
    if username<1:
        return None
    cursor=conn.cursor()
    try:
        args = [username,0]
        result_args = cursor.callproc('uspgetuserpasswordByName', args)
        #sql="SELECT Password FROM userdb.userinfo WHERE Username =%(uname)s "
        #data={"uname":username}
        #cursor.execute(sql,data)
        cursor.close()
        result=result_args[1]
        if result is not None:
            return result
        else:
            return None;
    except:
        print(exc_info())
        cursor.close()
        return None;

def saveUserKeys(userid,priv_pem,pub_pem):
    if userid<1:
        return False
    cursor=conn.cursor()
    try:
        args = [priv_pem,pub_pem,userid]
        result_args = cursor.callproc('uspsaveUserKeys', args)
        # sql=("Update userdb.userinfo "
        #      " SET Private_key=%(prv)s, Public_key=%(pub)s "
        #      " WHERE ID=%(uid)s")
        # data={'uid':userid, 'prv':priv_pem,'pub':pub_pem}
        # cursor.execute(sql,data)
        result=cursor.rowcount
        conn.commit()
        cursor.close()
        if (result>0):
            return True
        else:
            return False
    except:
        print (exc_info())
        conn.rollback()
        cursor.close()
        return False;

def getUserPubkey(userid):
    if userid<1:
        return None
    cursor=conn.cursor()
    try:
        args = [userid,0]
        result_args = cursor.callproc('uspgetUserPubkey', args)
        # sql="SELECT Public_key FROM userdb.userinfo WHERE ID =%(uid)s "
        # data={"uid":userid}
        # cursor.execute(sql,data)
        result=result_args[1]
        if result is not None:
            cursor.close()
            return result
        else:
            cursor.close()
            return None
    except:
        print(exc_info())
        cursor.close()
        return None


def getUserPrivatekey(userid):
    if userid<1:
        return None
    cursor=conn.cursor()
    try:
        args = [userid,0]
        result_args = cursor.callproc('uspgetUserPrivatekey', args)
        # sql="SELECT Private_key FROM userdb.userinfo WHERE ID =%(uid)s "
        # data={"uid":userid}
        # cursor.execute(sql,data)
        result=result_args[1]
        if result is not None:
            cursor.close()
            return result
        else:
            cursor.close()
            return None;
    except:
        print(exc_info())
        cursor.close()
        return None;

def followerCount(uid):
    if uid == 0:
        return None
    cursor=conn.cursor()
    try:
        args = [uid,0]
        result_args = cursor.callproc('uspgetUserPrivatekey', args)
        # sql=("select count(user1ID) from userrelation"
        #      " where User2ID=%(uid)s")
        # data={"uid":uid}
        # cursor.execute(sql,data)
        result=result_args[1]
        if result is not None and result>0:
            return (result-1)
        else:
            return 0
    except:
        print (exc_info())
        return 0
    finally:
        cursor.close()


def followingCount(uid):
    if uid == 0:
        return None
    cursor=conn.cursor()
    try:
        args = [uid,0]
        result_args = cursor.callproc('uspfollowingCount', args)
        # sql=("select count(user2ID) from userrelation"
        #      " where User1ID=%(uid)s")
        # data={"uid":uid}
        # cursor.execute(sql,data)
        result=result_args[1]
        if result is not None and result>0:
            return (result-1)
        else:
            return 0
    except:
        print (exc_info())
        return 0
    finally:
        cursor.close()


def postCount(uid):
    if uid == 0:
        return None
    cursor=conn.cursor()
    try:
        args = [uid,0]
        result_args = cursor.callproc('usppostCount', args)
        # sql=("select count(*) from userdb.Photos"
        #      " where uid=%(uid)s")
        # data={"uid":uid}
        # cursor.execute(sql,data)
        result=result_args[1]
        if result is not None and result>0:
            return result
    except:
        print (exc_info())
        return None
    finally:
        cursor.close()

def getUserToken(userid):
    cursor=conn.cursor()
    try:
        args = [userid,0]
        result_args = cursor.callproc('uspgetUserToken', args)
        # sql=("select accessToken from userdb.userinfo "
        #     "where ID =%(uid)s)")
        # data={'uid':userid}
        # cursor.execute(sql,data)
        result=result_args
        cursor.close()
        return result
    except:
        print (exc_info())
        cursor.close()
        return None

def updateUserToken(userid, token):
    if userid<0:
        return False
    else:
        cursor=conn.cursor()
        try:
            args = [token, userid]
            result_args = cursor.callproc('uspupdateUserToken', args)
            # sql=("Update userdb.userinfo "
            #      " SET accessToken=%(token)s "
            #      " WHERE ID=%(uid)s")
            # data={'uid':userid, 'token':token}
            # cursor.execute(sql,data)
            result=cursor.rowcount
            conn.commit()
            cursor.close()
            if (result>0):
                return True
            else:
                return False
        except:
            print (exc_info())
            conn.rollback()
            cursor.close()
            return False;



def getUserProfilePhoto(uid):
    if uid==0:
        return None
    try:
        cursor = conn.cursor()
        args = [uid,'','',0]
        result_args = cursor.callproc('uspgetUserProfilePhoto', args)
        # sql = ("select Path, Filename,UID from userdb.photos "
        #        "where ID = (select photoid from userdb.profilePhoto where userid=%(uid)s)")
        # data = {'uid':uid}
        # cursor.execute(sql,data)
        #Pics=cursor.fetchall()
        cursor.close()
    except:
        print (exc_info())
    if result_args[1] is not None and  result_args[2] is not None:
        import os
        url=os.path.join(result_args[1],result_args[2])
        return url
    else:
        return '' #should return default profile img



def getUserProfile(uid):
    if uid==0:
        return None
    cursor=conn.cursor()
    try:
        args = [uid,'','','','','','','']
        result_args = cursor.callproc('uspgetUserProfile', args)

        # sql=("select username,location,brithday,Gender,Occupation,Height,Weight from userdb.userdetails"
        #      " where userdetails.id=%(uid)s")
        # data={"uid":uid}
        # cursor.execute(sql,data)
        #row=cursor.fetchall()
        if result_args is not None:
            result=dict(username=result_args[1],location=result_args[2],brithday=result_args[3],Gender=result_args[4],
                        Occupation=result_args[5],Height=result_args[6],Weight=result_args[7])
    except:
        print (exc_info())
        return None
    finally:
        cursor.close()
    return result



def addUserProfile(uid,Uname,Location,brithday,Gender,Occupation,Height,Weight):
    if uid==0:
        return None
    cursor=conn.cursor()
    try:
        isExist=0
        args = [uid,Uname,Location,brithday,Gender,Occupation,Height,Weight,isExist]
        result_args = cursor.callproc('uspaddUserProfile', args)
        conn.commit()
        cursor.close()
        # sql=("insert into userdb.userDetails (UserId,username,location,brithday,Gender,Occupation,Height,Weight)"
        #     " Values(%(uid)s, %(uname)s, %(loca)s, %(brith)s, %(Gender)s, %(Occup)s, %(Height)s, %(Weight)s)")
        # data={"uid":uid, "uname":Uname,"loca":Location,"brith":datetime.strptime(brithday,'%Y-%m-%d'),"Gender":Gender,"Occup":Occupation,"Height":Height,"Weight":Weight}
        # cursor.execute(sql,data)
        # row=cursor.rowcount
        if result_args[8] is not None:
            isExist=result_args[8]
        else:
            isExist=False


        if isExist == 0:
            return True
        else:
            return False
    except:
        print (exc_info())
        conn.rollback()
        cursor.close()
        return False

def updateUserProfile(uid,Uname,Location,brithday,Gender,Occupation,Height,Weight):
    if uid==0:
        return None
    cursor=conn.cursor()
    try:
        args = [uid,Uname,Location,brithday,Gender,Occupation,Height,Weight]
        result_args = cursor.callproc('uspupdateUserProfile', args)

        # sql=("Update userdetails "
        #     "set Username=%(uname)s,Location=%(loca)s,Brithday=%(brith)s,Gender=%(Gender)s,Occupation=%(Occup)s,"
	     #    "Height=%(Height)s,Weight=%(Weight)s "
        #     "Where UserID=%(uid)s")
        # data={"uid":uid, "uname":Uname,"loca":Location,"brith":datetime.strptime(brithday,'%Y-%m-%d'),"Gender":Gender,"Occup":Occupation,"Height":Height,"Weight":Weight}
        # cursor.execute(sql,data)
        # row=cursor.rowcount
        conn.commit()
        cursor.close()
        return True
    except:
        print (exc_info())
        conn.rollback()
        cursor.close()
        return False

#addUserProfile(4,"test1","ny","1982-07-02","M","worker","180","150")

#updateUserProfile(4,"test1","ny","2001-01-01","F","Test","190","160")

def getUserPosts(uid):
    result=list()
    if uid == 0:
        return None
    cursor=conn.cursor()
    try:
        #cannot use stored procedure, the procedure cannot return multiple rows in this case, or create a temp table in the procedure and select from that temp table.
        #todo: need to improvde the procedure
        sql=("select id from userdb.Photos"
             " where uid=%(uid)s and removed=0")
        data={"uid":uid}
        cursor.execute(sql,data)
        rows=cursor.fetchall()
        if rows is not None and len(rows)>0:
            for e in rows:
                result.append(e[0])
    except:
        print (exc_info())
    finally:
        cursor.close()

    return result

def getUserFavioritePic(uid):
    result=list()
    cursor=conn.cursor()
    try:
        #cannot use stored procedure, the procedure cannot return multiple rows in this case, or create a temp table in the procedure and select from that temp table.
        #todo: need to improvde the procedure
        sql=("select photoid from Favorite "
             " where userid=%(uid)s")
        data={"uid":uid}
        cursor.execute(sql,data)
        rows=cursor.fetchall()
        if rows is not None and len(rows)>0:
            for e in rows:
                result.append(e[0])
    except:
        print (exc_info())
    finally:
        cursor.close()

    return result

#endregion


#region: Photo and Comments

def addphoto(UID, PName, PDesc, PPath, FiName):
    newCursor = conn.cursor();
    try:
        if (UID <= 0):
            return 0;
        args = [UID, PName, PDesc, PPath, FiName, 0]
        result_args = newCursor.callproc('uspAddPhoto', args)
        conn.commit()
        newCursor.close()
        return (result_args[5])
    except Error as e:
        conn.rollback()
        print(e)
        newCursor.close()
    return 0;

def removePhoto(UID, Pic_id):
    newCursor=conn.cursor();
    try:
        if (UID <= 0):
            return False
        args = [UID, Pic_id]
        result_args=newCursor.callproc('uspRemovePhoto',args)
        conn.commit()
        newCursor.close()
        return True
    except Error as e:
        conn.rollback()
        print e
        newCursor.close()
    return False

def addphotoTags(Pid,Tags):
    newCursor=conn.cursor();
    try:
        for tag in Tags:
            tagid=tag['tagid']
            if (tagid == 0):
                tagid=addNewTag(tag['text'])
            args = [Pid,tagid,tag['left'],tag['top']]
            result_args = newCursor.callproc('uspaddphotoTags', args)
            # sql=("Insert into PhotoTags (PhotoID,TagID,LeftX,TopY)"
            #          "Values(%(pic)s, %(tag)s, %(x)s,%(y)s)")
            # data={'pic':Pid, 'tag':tagid,'x':tag['left'],'y':tag['top']}
            # newCursor.execute(sql,data)
            result=newCursor.rowcount
        conn.commit()
        newCursor.close()
        return True
    except Error as e:
        conn.rollback()
        print (e)
        newCursor.close()
    return False;


def addNewTag(tagText):
    newCursor=conn.cursor();
    try:
        args = [tagText, 0]
        result_args = newCursor.callproc('uspAddTag', args)
        conn.commit()
        if result_args[1]>0:
            return result_args[1]
    except Error as e:
        conn.rollback()
        print (e)
        newCursor.close()
    return 0;




def addcomment(CText, UID, PID):
    if UID==0 or PID==0 or CText is None:
        return
    if len(CText) <1:
        return
    cursor = conn.cursor()
    try:

        args = [CText, UID, PID, 0]
        result_args = cursor.callproc('uspAddComment', args)
        conn.commit()
        #print(result_args[4])
        return result_args[3]
    except Error as e:
        conn.rollback()
        print(e)
    finally:
        cursor.close()

def removeComment(userid, pic_id, comment_id):
    if (userid<1 or pic_id<1):
        return False;
    try:
        cursor=conn.cursor()
        args = [comment_id]
        result_args = cursor.callproc('uspremoveComment', args)
        # sql="Delete FROM userdb.comments where ID=%(c_id)s"
        # data={'c_id':comment_id}
        # cursor.execute(sql,data)
        #result=cursor.fetchall()
        cursor.close()
        conn.commit()
        return True
    except:
        print (exc_info())
        conn.rollback()
        return False

def getPicComments(pic_id):
        try:
            pic_comments=list()
            cursor = conn.cursor()
            sql = ("select Username, Context, comments.AddDate from userdb.comments,userdb.userinfo "
                   "where PhotoID = %(pid)s and userinfo.id=comments.UserID")
            data = {'pid':pic_id}
            cursor.execute(sql,data)
            comments=cursor.fetchall()
            cursor.close()
            if len(comments) >0:
                for comment in comments:
                    com=dict(username=comment[0],comment=comment[1],time=comment[2].strftime("%Y-%m-%d %H:%M:%S"))
                    pic_comments.append(com)
        except:
            print (exc_info())
            pic_comments=list()
        return pic_comments


def AddLike(UID, PID):
    if UID==0 or PID==0:
        return
    try:
        cursor = conn.cursor()
        args = [UID, PID, 0]
        result_args = cursor.callproc('uspAddLike', args)
        conn.commit()
        return True
        # print(result_args[3])
    except Error as e:
        conn.rollback()
        print(e)
        return False
    finally:
        cursor.close()
        # conn.close()

def UnlikePic(UID,PID):
    if UID==0 or PID==0:
        return False
    try:
        cursor = conn.cursor()
        args = [UID, PID, 0]
        result_args = cursor.callproc('uspCancelLike', args)
        conn.commit()
        cursor.close()
        return True
        # print(result_args[3])
    except Error as e:
        conn.rollback()
        print(e)
        cursor.close()
        return False

def getlistcount(pic_id):
        try:
            cursor=conn.cursor()
            sql=("select count(id) from likes where PhotoID=%(pic)s")
            data={'pic':pic_id}
            cursor.execute(sql, data)
            result=cursor.fetchall()
            cursor.close()
            if (len(result))>0 and len(result)==1:
                return result[0][0]
        except:
            print (exc_info())
            return 0;

#endregion

def AddUserRelation(u1id, u2id, Rtype):
    if u1id ==0 or u2id==0:
        return
    success=False
    try:
        cursor = conn.cursor()
        args = [u1id, u2id, Rtype, 0]
        result_args = cursor.callproc('uspAddUserRelation', args)
        conn.commit()
        # print(result_args[3])
        success=True
    except Error as e:
        conn.rollback()
        print(e)
    finally:
        cursor.close()
        return success


def GetPassword(uid):
    try:
        cursor = conn.cursor()
        args = [uid, 0]
        result_args = cursor.callproc('uspGetPassword', args)
        #print(result_args[1])
        return result_args[1]
    except Error as e:
        print(e)
    finally:
        cursor.close()
        # conn.close()

def getFeedsFromDb(uid):
    result=list()
    if uid ==0:
        return None
    try:
        cursor = conn.cursor()
        sql=("select photos.id as PhotoId from photos where photos.uid in (select userrelation.user2ID from userrelation"
             " where User1ID=%(uid)s) and removed=0 order by PAddDate desc")
        data={"uid":uid}
        cursor.execute(sql,data)
        rows=cursor.fetchall()
        cursor.close()
        for row in rows:
            if row[0] is not None:
                result.append(row[0])
        return result
    except:
            print (exc_info())

def searchProduct(keyword):
    try:
        cursor=productConn.cursor()
        sql=("select ID, Brand_id, ProductType_id, Name from productdb.Products where Brand_ID in (select Brand_ID from productdb.Brands where BrandName like CONCAT('%', %(key)s, '%'))"
						"or	ProductType_ID in (select ProductType_ID from productdb.productTypes where TypeName like concat('%',%(key)s,'%')"
                        "or  Name like concat('%',%(key)s,'%'))")
        data={"key":keyword}
        cursor.execute(sql,data)
        result=cursor.fetchall()
        cursor.close()
        if (result is not None):
            return result
    except:
        print(exc_info())
        cursor.close()

def get_product_detail(id):
    if (id<1):
        return
    try:
        cursor=productConn.cursor()
        sql=("select Value as price from Productdb.productdetail where ProductID=%(pid)s")
        data={"pid":id}
        cursor.execute(sql,data)
        result=cursor.fetchall()
        cursor.close()
        return result
    except:
        print (exc_info())
        cursor.close()

def get_product_brand(id):
    if (id<1):
        return
    try:
        cursor=productConn.cursor()
        sql=("select brandname from productdb.brands where brand_id=%(bid)s")
        data ={"bid":id}
        cursor.execute(sql,data)
        result=cursor.fetchall()
        cursor.close()
        return result
    except:
        print (exc_info())
        cursor.close()

def get_product_link(id):

    if (id<1):
        return
    try:
        cursor=productConn.cursor()
        sql=("select Url from Productdb.links where ProductID=%(pid)s")
        data={"pid":id}
        cursor.execute(sql,data)
        result=cursor.fetchall()
        cursor.close()
        return result;
    except:
        print (exc_info())
        cursor.close()

def addPhotoFavoriteToDB(userid, photoid):
    cursor=conn.cursor()
    from datetime import datetime
    try:
        if cursor is not None:
            args = [userid, photoid, 0]
            result_args = cursor.callproc('uspaddPhotoFavoriteToDB', args)
            conn.commit()
            cursor.close()
            return True
            # sql = ("select * from favorite where Userid=%(uid)s and Photoid=%(pic)s")
            # data={'uid':userid, 'pic':photoid}
            # cursor.execute(sql,data)
            # result=cursor.fetchall()
            # if (len(result)>0):
            #     return True
            # else:
            #     sql=("Insert into favorite "
            #          "Values(%(uid)s, %(pic)s, %(time)s)")
            #     data={'uid':userid, 'pic':photoid,'time':datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            #     cursor.execute(sql,data)
            #     result=cursor.rowcount
            #     conn.commit()
            #     cursor.close()
            #     if (result>0):
            #         return True
            #     else:
            #         return False;
    except:
        print (exc_info())
        conn.rollback()
        cursor.close()
        return False

#addPhotoFavoriteToDB(2,91)


# a=sess.query(Photos).all()
# output="PhotoID:{ID}; Description:{Description}"
# print  output.format(ID=a[0].ID, Description=a[0].Description)
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

'''
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    password = Column(String)


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    image = Column(String)
    source_url = Column(String)
    message = Column(String)
    pin_count = Column(Integer, default=0)
'''

'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    image = models.ImageField(upload_to='items')
    source_url = models.TextField()
    message = models.TextField(blank=True, null=True)
    pin_count = models.IntegerField(default=0)
'''
    # class Meta:
    #    db_table = 'pinterest_example_item'

'''
class Board(Base):
    __tablename__ = 'board'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String)
    description = Column(String)
    slug = Column(String)
'''

'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField()
'''

'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    item = models.ForeignKey(Item)
    board = models.ForeignKey(Board)
    influencer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='influenced_pins')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
'''

'''
class Follow(Base):


    __tablename__ = 'Follow'
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user.id'))
    target = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=func.now())
'''

'''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='following_set')
    target = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='follower_set')
    created_at = models.DateTimeField(auto_now_add=True)
'''

'''
stmt = text("""select *
               from test_usertable
               where username=:username""")
            # s is instance of Session() class factory
            '''
# results = sess.execute(stmt, params=dict(username=username))


##result=AddNewUser('username','123123','w13se123','asdf@asdf.com')
#print result


#
# cnx = mysql.connector.connect(user="allen",password="yao0702",host="localhost",database="userdb")
# cursor = cnx.cursor()
# cursor.callproc("uspTest_usertable",args=("allen5","allenTest"))
# #cursor.execute("select * from test_usertable")
# #cursor.fetchall()
# cnx.commit()

# results = exec_procedure(sess,"uspTest_usertable",['allen2','allenpw'], **t)
# results = exec

# sess.execute("select * from test_usertable")
# Base.metadata.create_all(engine)