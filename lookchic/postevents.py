__author__ = 'zoe'
from sys import exc_info


def addphotoEvent(userid, RelativePath, Saved_file_name, tags):
    if userid > 0 and RelativePath != '' and Saved_file_name != '':
        from models import addphoto, addphotoTags
        pic_id = addphoto(userid, 'photoname', 'photoDescription', RelativePath, Saved_file_name)
        if pic_id>0:
            addphotoTags(pic_id,tags)

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

def removePhotoEvent(userid, pic_id):
    if (userid>0 and pic_id>0):
        from models import removePhoto
        result=removePhoto(userid,pic_id)
        if result is True:
            from pin_feed import User
            user_pin = User(userid)
            from feed_managers import manager
            manager.remove_user_activity(userid,user_pin.add_pic(pic_id))
            return True
        else:
            return False

#todo: return comment list after add comment
def adduserComment(userid, pic_id, comment):
    from models import addcomment,getPicComments
    newCommentList=list()
    if (userid > 0 and pic_id > 0 and comment != ''):
        try:
            result=addcomment(comment, userid, pic_id)
            if result is not None:
                newCommentList=getPicComments(pic_id)
                return newCommentList
            else:
                return None
        except:
            print (exc_info())
            return None


#todo: return comment list after remove comment
def removeuserComment(userid, pic_id,comment_id):
    from models import removeComment,getPicComments
    if (userid>0 and pic_id>0):
        try:
            result=removeComment(userid, pic_id,comment_id)
            if result is True:
                newCommentlist=getPicComments(pic_id)
                return newCommentlist
            else:
                return None
        except:
            print (exc_info())
            return None


def loaduserFeeds(userid, page):
    result = list()
    from models import getFeedsFromDb
    temp_list = getFeedsFromDb(userid)
    #print temp_list
    if page == 1:
        from enrichlist import UserContent, richUserPictures
        user = UserContent(userid)
        content = richUserPictures(user.Pop())
        result.extend(generateFeeds(content.pics))
    else:
        from models import getFeedsFromDb
        from enrichlist import UserContent, richUserPictures
        db_feedList = getFeedsFromDb(userid)
        content = richUserPictures(db_feedList,userid)
        result.extend(generateFeeds(content.pics))
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
        userProfile = getUserProfile(userid)
        followers = followerCount(userid)
        followings = followingCount(userid)
        posts = postCount(userid)
        favorites = getUserFavorite(userid)
        userPosts = getUserPosts(userid)
        userProfilePhoto = getUserProfilePhoto(userid)
        feeds=list()
        if (userPosts is not None):
            content = richUserPictures(userPosts,userid)
            feeds.extend(generateFeeds(content.pics))
        result = dict(userProfile=userProfile,userProfileUrl=userProfilePhoto,followers=followers,followings=followings,posts=posts, favorites=favorites,userFeeds=feeds)
        return result

def addUserLikePhoto(userid, photoid):
    if userid is not None and photoid is not None:
        from models import AddLike,getlistcount,UnlikePic
        result=AddLike(userid,photoid)
        if result is True:
            count=getlistcount(photoid)
            return count

    else:
        return None


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
            feeds=generateFeeds(content.pics)
            result.extend(feeds)
    return result

def UpdateUserProfile(uid,Uname,Location,brithday,Gender,Occupation,Height,Weight):
    if (uid==0):
        return False
    else:
        from models import updateUserProfile
        result=updateUserProfile(uid,Uname,Location,brithday,Gender,Occupation,Height,Weight)
        return result

def generateFeeds(pics):
    result=list()
    if pics is not None:
        for pic in pics:
            feed = dict(picid=pic.pic_id, picuid=pic.pic_uid, username=pic.pic_userName, avator=pic.pic_userProfileimg, url=pic.pic_url, time=pic.pic_time, comments=pic.commentList, likeCount=pic.likeCount, liked=pic.liked, tags=pic.tags)
            result.append(feed)

    return result
