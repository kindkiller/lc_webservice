__author__ = 'zoe'

from models import *
from feed_managers import manager
from sys import exc_info



class richPicture(object):
    pic_id=0
    pic_url=''
    pic_uid=0
    pic_userName=''
    pic_time=''
    commentList=list()
    def __init__(self,id,url,UID):
        self.pic_id=id
        self.pic_url=url
        self.pic_uid=UID
        print self.pic_id

        self.pic_userName=self.getUsername()
        self.pic_time=self.getTime()
        self.commentList=self.getPicComments()

    def getUsername(self):
        try:
            cursor = conn.cursor()
            sql = ("select username from userdb.userinfo where ID = %(uid)s")
            data = {'uid':self.pic_uid}
            cursor.execute(sql,data)
            usernames=cursor.fetchall()
            cursor.close()
            if usernames is not None:
                username=usernames.pop()
                return username[0]
        except:
            print (exc_info())


    def getTime(self):
        try:
            cursor = conn.cursor()
            sql = ("select PAddDate from userdb.photos where ID = %(pid)s")
            data = {'pid':self.pic_id}
            cursor.execute(sql,data)
            times=cursor.fetchall()
            cursor.close()
            if times is not None:
                time=times.pop()
                return time[0].strftime("%B,%d,%Y")
        except:
            print (exc_info())
            return null

    def getPicComments(self):
        try:
            cursor = conn.cursor()
            sql = ("select UserID, Context, AddDate from userdb.comments where PhotoID = %(pid)s")
            data = {'pid':self.pic_id}
            cursor.execute(sql,data)
            comments=cursor.fetchall()
            cursor.close()
            if len(comments) >0:
                for comment in comments:
                    com=richComment(comment[0],comment[1],comment[2].strftime("%B,%d,%Y"))
                    self.commentList.append(com)
        except:
            print (exc_info())
            self.commentList=list()



class richComment(object):
    UID=0
    Context=''

    def __init__(self, uid, context,time):
        self.UID=uid
        self.Context=context
        self.Time=time

class richUserPictures(object):


    def __init__(self, pic_ids):
        self.pics=list()
        from sys import exc_info
        try:
            self.pics=self.enrichPictures(pic_ids)
        except:
            print (exc_info())


    def enrichPicture(self,pic_id):
        try:
            cursor = conn.cursor()
            sql = ("select Path, Filename,UID from userdb.photos where ID = %(pid)s")
            data = {'pid':pic_id}
            cursor.execute(sql,data)
            Pics=cursor.fetchall()
            cursor.close()
        except:
            print (exc_info())

        if len(Pics)>0:
            for pic in Pics:
                import os
                url=os.path.join(pic[0],pic[1])
                picture=richPicture(pic_id,url,pic[2])
                return picture

    def enrichPictures(self,pic_ids):
        self.pics=list()
        for pic_id in pic_ids:
            pic=self.enrichPicture(pic_id)
            if pic is not None:
                self.pics.append(pic)
        return self.pics


class UserContent(object):

    def __init__(self, user_id):
        self.userID=user_id
        #pics=list()

        feeds=manager.get_feeds(user_id)['normal']
        #feeds.delete()
        self.ContentList=list()
        for feed in list(feeds[:25]):
            from stream_framework.activity import  Activity
            if feed.verb.id==4:
                #print feed
                self.ContentList.append(feed.object_id)

    def Pop(self):
        return self.ContentList


from models import addphoto, AddComment

#addphoto(UID=1,PName='pic',PDesc='picDesc',PPath='\df',FiName='filename')



