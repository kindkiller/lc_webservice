__author__ = 'zoe'

from models import *
from feed_managers import manager


class richPicture(object):
    pic_id=0
    pic_url=''
    pic_uid=0
    commentList=list()
    def __init__(self,id,url,UID):
        self.pic_id=id
        self.pic_url=url
        self.pic_uid=UID
        self.commentList=self.getPicComments()


    def getPicComments(self):
        comments=sess.query(Comments).filter(Comments.PhotoID==self.pic_id).all()
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
        self.pics=self.enrichPictures(pic_ids)

    def enrichPicture(self,pic_id):
        Pics=sess.query(Photos).filter(Photos.ID==pic_id).all()
        if len(Pics)>0:
            for pic in Pics:
                picture=richPicture(pic.ID,pic.Path,pic.UID)
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
        feeds=manager.get_feeds(user_id)['normal']
        #feeds.delete()
        self.ContentList=list()
        for feed in list(feeds[:25]):
            from stream_framework.activity import  Activity
            if feed.verb.id==5:
                #print feed
                self.ContentList.append(feed.object_id)

    def Pop(self):
        return self.ContentList


from models import AddPhoto, AddComment

#AddPhoto(UID=1,PName='pic',PDesc='picDesc',PPath='\df',FiName='filename')


userContent=UserContent(2)
pics=richUserPictures(userContent.Pop())
for pic in pics.pics:
    print pic
