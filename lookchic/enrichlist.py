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
            picSession=Session()
            username=picSession.query(Userinfo).filter(Userinfo.ID==self.pic_uid).first()
        except:
            print (exc_info())
        if username is not None:
            return username.Username

    def getTime(self):
        try:
            picSession=Session()
            time=picSession.query(Photos).filter(Photos.ID==self.pic_id).first()
        except:
            print (exc_info())

        if time is not None:
            return time.PAddDate.strftime("%B,%d,%Y")

    def getPicComments(self):
        try:
            picSession=Session()
            comments=picSession.query(Comments).filter(Comments.PhotoID==self.pic_id).all()
        except:
            print (exc_info())
        if len(comments) >0:
            for comment in comments:
                com=richComment(comment.UserID,comment.Context,comment.AddDate)
                self.commentList.append(com)


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
            picSession=Session()
            Pics=picSession.query(Photos).filter(Photos.ID==pic_id).all()
        except:
            print (exc_info())

        if len(Pics)>0:
            for pic in Pics:
                import os
                url=os.path.join(pic.Path,pic.Filename)
                picture=richPicture(pic.ID,url,pic.UID)
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


from models import AddPhoto, AddComment

#AddPhoto(UID=1,PName='pic',PDesc='picDesc',PPath='\df',FiName='filename')



