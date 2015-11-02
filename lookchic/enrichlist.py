__author__ = 'zoe'

from models import *
from feed_managers import manager
from sys import exc_info



class richPicture(object):
    pic_id=0
    pic_url=''
    pic_uid=0
    pic_userName=''
    pic_userProfileimg=''
    pic_time=''
    likeCount=0
    liked=0
    commentList=list()
    tags=list()
    def __init__(self,id,url,UID, userid):
        self.pic_id=id
        self.pic_url=url
        self.pic_uid=UID
        self.userid=userid

        #print self.pic_id

        self.pic_userName=self.getUsername()
        self.pic_userProfileimg=getUserProfilePhoto(UID)
        self.pic_time=self.getTime()
        self.commentList=self.getPicComments()
        self.likeCount=self.getlistcount()
        self.liked=self.isLiked()
        self.tags=self.getPhotoTags()

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
            pic_comments=list()
            cursor = conn.cursor()
            sql = ("select Username, Context, comments.AddDate from userdb.comments,userdb.userinfo "
                   "where PhotoID = %(pid)s and userinfo.id=comments.UserID")
            data = {'pid':self.pic_id}
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

    def getPhotoTags(self):
        try:
            tags=list()
            cursor = conn.cursor()
            sql = ("select Tag_Text, LeftX, TopY from userdb.phototags,tags"
                    " where phototags.TagID=tags.ID and phototags.PhotoID=%(pid)s")
            data = {'pid':self.pic_id}
            cursor.execute(sql,data)
            rows=cursor.fetchall()
            cursor.close()
            if len(rows) >0:
                for row in rows:
                    com=dict(text=row[0],left=row[1],top=row[2])
                    tags.append(com)
        except:
            print (exc_info())
            tags=list()
        return tags

    def getlistcount(self):
        try:
            cursor=conn.cursor()
            sql=("select count(id) from likes where PhotoID=%(pic)s")
            data={'pic':self.pic_id}
            cursor.execute(sql, data)
            result=cursor.fetchall()
            cursor.close()
            if (len(result))>0 and len(result)==1:
                return result[0][0]
        except:
            print (exc_info())
            return 0;

    def isLiked(self):
        try:
            cursor=conn.cursor()
            sql=("select count(id) from likes where PhotoID=%(pic)s and UserID=%(uid)s")
            data={'pic':self.pic_id, 'uid':self.userid}
            cursor.execute(sql, data)
            result=cursor.fetchall()
            cursor.close
            if (len(result))>0 and len(result)==1:
                return 1
        except:
            print (exc_info())
            return 0;

class richComment(object):
    UID=0
    Context=''

    def __init__(self, uid, context,time):
        self.UID=uid
        self.Context=context
        self.Time=time

class richUserPictures(object):


    def __init__(self, pic_ids, userid):
        self.pics=list()
        self.userid=userid
        from sys import exc_info
        try:
            self.pics=self.enrichPictures(pic_ids)
        except:
            print (exc_info())


    def enrichPicture(self,pic_id):
        try:
            cursor = conn.cursor()
            sql = ("select Path, Filename,UID from userdb.photos where ID = %(pid)s and removed=0")
            data = {'pid':pic_id}
            cursor.execute(sql,data)
            Pics=cursor.fetchall()
            cursor.close()
            if len(Pics)>0:
                for pic in Pics:
                    import os
                    url=os.path.join(pic[0],pic[1])
                    picture=richPicture(pic_id,url,pic[2], self.userid)
                    return picture
        except:
            print (exc_info())
            cursor.close()
            return None

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
            from stream_framework.activity import Activity
            if feed.verb.id==4:
                #print feed
                self.ContentList.append(feed.object_id)

    def Pop(self):
        return self.ContentList




#result=richPicture(87,'12311',1)
#print result
####
#addphoto(UID=1,PName='pic',PDesc='picDesc',PPath='\df',FiName='filename')



