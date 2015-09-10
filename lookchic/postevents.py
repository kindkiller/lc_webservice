__author__ = 'zoe'
from sys import exc_info


def addphotoEvent(userid, RelativePath, Saved_file_name):
    if userid > 0 and RelativePath != '' and Saved_file_name != '':
        from models import addphoto
        pic_id = addphoto(userid, 'photoname', 'photoDescription', RelativePath, Saved_file_name)
        if pic_id>0:
            from pin_feed import User
            user_pin = User(userid)
            # user_pin.add_pic(pic_id)
            from feed_managers import manager
            manager.add_user_activity(userid, user_pin.add_pic(pic_id))
            #feeds = manager.get_feeds(1)['normal']
            #print (feeds[:])
        return pic_id
    else:
        return 0


def adduserComment(userid, pic_id, comment):
    from models import addcomment
    if (userid > 0 and pic_id > 0 and comment != ''):
        try:
            result = addcomment(comment, userid, pic_id)
            return result
        except:
            print (exc_info())
            return 0

def removeuserComment(userid, pic_id,comment_id):
    from models import removeComment
    if (userid>0 and pic_id>0):
        try:
            result=removeComment(userid, pic_id,comment_id)
            return result
        except:
            print (exc_info())
            return False

def loaduserFeeds(userid, page):
    result = list()
    from models import getFeedsFromDb
    temp_list = getFeedsFromDb(userid)
    #print temp_list
    if page == 1:
        from enrichlist import UserContent, richUserPictures
        user = UserContent(userid)
        content = richUserPictures(user.Pop())
        for pic in content.pics:
            feed = dict(picid=pic.pic_id, picuid=pic.pic_uid, username=pic.pic_userName, url=pic.pic_url, time=pic.pic_time,comments=pic.commentList, likeCount=pic.likeCount,  liked=pic.liked)
            result.append(feed)
    else:
        from models import getFeedsFromDb
        from enrichlist import UserContent, richUserPictures
        db_feedList = getFeedsFromDb(userid)
        content = richUserPictures(db_feedList,userid)
        for pic in content.pics:
            feed = dict(picid=pic.pic_id, picuid=pic.pic_uid, username=pic.pic_userName, url=pic.pic_url, time=pic.pic_time, comments=pic.commentList, likeCount=pic.likeCount, liked=pic.liked)
            result.append(feed)
    return result

def addPhotoFavorite(userid, photoid):
    if userid <=0 or photoid<=0:
        return False
    else:
        from models import addPhotoFavoriteToDB
        result=addPhotoFavoriteToDB(userid, photoid)
        return result

def getUserProfilePage(userid):
    if userid<=0:
        return None;
    else:
        from models import followerCount,followingCount,postCount,getUserPosts,getUserProfile,getUserProfilePhoto
        from enrichlist import UserContent, richUserPictures
        userProfile=getUserProfile(userid)
        followers=followerCount(userid)
        followings=followingCount(userid)
        posts=postCount(userid)
        favorites=getUserFavorite(userid)
        userPosts=getUserPosts(userid)
        userProfilePhoto=getUserProfilePhoto(userid)
        feeds=list()
        if (userPosts is not None):
            content = richUserPictures(userPosts,userid)
        for pic in content.pics:
            feed = dict(picid=pic.pic_id, picuid=pic.pic_uid, username=pic.pic_userName, url=pic.pic_url, time=pic.pic_time, comments=pic.commentList, likeCount=pic.likeCount, liked=pic.liked)
            feeds.append(feed)
        result=dict(userProfile=userProfile,userProfileUrl=userProfilePhoto,followers=followers,followings=followings,posts=posts, favorites=favorites,userFeeds=feeds)
        return result



def getUserFavorite(userid):
    result=list()
    if userid<=0:
        return None
    else:
        from models import getUserFavioritePic
        from enrichlist import UserContent, richUserPictures
        favioriteList=getUserFavioritePic(userid)
        if favioriteList is not None:
            content = richUserPictures(favioriteList,userid)
        for pic in content.pics:
            feed = dict(picid=pic.pic_id, picuid=pic.pic_uid, username=pic.pic_userName, url=pic.pic_url, time=pic.pic_time, comments=pic.commentList, likeCount=pic.likeCount, liked=pic.liked)
            result.append(feed)
    return result

aa=getUserProfilePage(2)
print aa
##result=removeuserComment(1,87,2)
#print result