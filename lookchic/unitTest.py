# -*- coding: utf-8 -*-

#from feed_managers import manager
import celery
import mysql.connector
from stream_framework.feed_managers.base import Manager
from stream_framework.feed_managers.base import FanoutPriority
from stream_framework.feeds.redis import RedisFeed
from stream_framework.activity import Activity
from pin_feed import PinFeed
from pin_feed import AggregatedPinFeed
from pin_feed import UserPinFeed
from feed_managers import manager
from stream_framework.verbs.base import Follow as verbFollow,Add,Love,Comment
from models import User as UserModel,Item, Pin, Follow,userDB_engine, Userdetails,UserRelation,sess
from models import *
from sqlalchemy.orm import sessionmaker
from celery import Celery

#Session = sessionmaker(bind=engine)

#session=Session()
'''
class User(UserPinFeed):

    def create_pic(self,pic_id):
        self.pic_id=pic_id



    def create_user(self,id,name):
        newUser=Userinfo(Username=name, )
        self.user_id=id
        self.name=name
        return self

    def create_comment(self,id,pic_id):
        self.comment_id=id

    def get_user_id(self):
        return self.user_id

    def create_activity(self):
        from stream_framework.activity import Activity
        from stream_framework.verbs.base import Follow,Add,Love,Comment
        activity = Activity(
            self.user_id,
            Love,
            12,
            3,
            time=None,
            extra_context=dict(item_id=self.user_id)
        )
        return activity
         #Activity(self.user_id,Add,self.pic_id)

    def add_pic(self):
        from stream_framework.activity import Activity
        from stream_framework.verbs.base import Follow,Add,Love,Comment

        return Activity(self.user_id,Add,self.pic_id)

    def Follow(self,target_id):
        a=UserRelation(User1ID=self.user_id,User2ID=target_id,Type=1)
        sess.add(a)
        sess.commit()
        return Activity(self.user_id, verbFollow,target_id)

    def add_comment(self,pic_id):
        comment=Comment(201,'comment')
        return Activity(self.user_id,Comment, comment, pic_id)
'''


class Comment(object):

    def __init__(self,comment_id,comment):
        self.id=comment_id
        self.comment=comment

'''
class PinManager(Manager):
            # customize the feed classes we write to
            feed_classes = dict(
                normal=User,
                aggregated=AggregatedPinFeed
            )
            # customize the user feed class
            user_feed_class = User

            # define how stream_framework can get the follower ids
            #def get_user_follower_ids(self, user_id):
                #ids = Follow.objects.filter(target=user_id).values_list('user_id', flat=True)
                #return {FanoutPriority.HIGH:ids}

            # utility functions to easy integration for your project
            def add_pic(self, pin):
                activity=pin.add_pic()
                self.add_user_activity(pin.user_id,activity)

            def add_pin(self, pin):
                activity = pin.create_activity()
                # add user activity adds it to the user feed, and starts the fanout
                self.add_user_activity(pin.user_id, activity)


            def add_comment(self, pin,pic_id):
                activity=pin.add_comment(pic_id)
                self.add_user_activity(pin.user_id,activity)

            def remove_pin(self, pin):
                activity = pin.create_activity()
                # removes the pin from the user's followers feeds
                self.remove_user_activity(pin.user_id, activity)

            def follow(self,actor,target):
                activity=actor.Follow(target.user_id)
                self.add_user_activity(actor.user_id,activity)

            def get_user_follower_ids(self,user_id):
                query=session.query(Follow).filter_by(user=user_id).all()
                follower_ids=[]
                for row in query:
                    follower_ids.append(row.target)
                return {FanoutPriority.HIGH:follower_ids}
'''

print userDB_engine
print sess


User1DB=UserModel(id=1,password=123)
#session.add(User1DB)
PinDB=Pin(id=11,user_id=1)
#session.add(PinDB)
itemDB=Item(id=101,user_id=1,image='img', pin_count=0)
#session.add(itemDB)

User1DB=UserModel(id=2,password=123)
#session.add(User1DB)
PinDB=Pin(id=12,user_id=1)
#session.add(PinDB)

itemDB=Item(id=102,user_id=2,image='img2', pin_count=0)
#session.add(itemDB)
#feeds= manager.get_feeds(1)['normal']
#feeds.delete()
#feeds= manager.get_feeds(2)['normal']
#feeds.delete()

from pin_feed import User
user1=User(1)
#user1.delete()
user1.create_pic(64)
user2=User(2)
#user2.delete()
user2.create_pic(12)
user2.create_comment(101,11)

#manager.follow_user(user2.user_id,user1.user_id)
#manager.follow_user(user1.user_id,user2.user_id)

# user3=User(3)
# user3.create_pic(13)
#
# user4=User(4)
# user4.create_pic(14)
#
# user5=User(5)
# user5.create_pic(15)

#manager.follow_user(user2.user_id,user1.user_id)
#session.add(Follow(user=user2.user_id,target=user1.user_id))
#manager.follow(user2, user1)
#session.add(Follow(user=user1.user_id,target=user2.user_id))
#manager.follow(user1, user2)
#manager.follow(user5, user1)
#manager.follow(user1, user4)


#manager.add_user_activity(user1.user_id,user1.add_pic(63))
#manager.add_user_activity(user2.user_id,user2.add_pic(64))
#manager.add_pin(user3)
#manager.add_pin(user4)
#manager.add_pin(user5)
#manager.add_comment(user2,11)


feeds= manager.get_feeds(1)['normal']
feeds2=manager.get_feeds(2)['normal']
#activities=list(feeds[1])
#print activities
#feeds.delete()
#feeds2.delete()

print 'output'
print feeds[:]
print feeds2[:]
print 'user1:'
print user1[:100]
print 'user2:'
print user2[:]
# print 'user3:'
# print user3[:]
# print 'user4:'
# print user4[:10]
# print 'user5:'
# print user5[:]




#user1.delete()
#user2.delete()
# user3.delete()
# user4.delete()
# user5.delete()


'''
feed.delete()
print 'output'
print feed.count()
print feed
'''


