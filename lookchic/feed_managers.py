# -*- coding: utf-8 -*-
from stream_framework.feed_managers.base import Manager
from stream_framework.feed_managers.base import FanoutPriority
from models import *
from pin_feed import AggregatedPinFeed, PinFeed, UserPinFeed, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class PinManager(Manager):
    # this example has both a normal feed and an aggregated feed (more like
    # how facebook or wanelo uses feeds)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    feed_classes = dict(
        normal=PinFeed,
        aggregated=AggregatedPinFeed
    )
    user_feed_class = UserPinFeed

    def add_pin(self, pin):
        activity = pin.create_activity()
        # add user activity adds it to the user feed, and starts the fanout
        self.add_user_activity(pin.user_id, activity)

    # def add_pic(self, pin):
    #             activity=pin.add_pic()
    #             self.add_user_activity(pin.user_id,activity)

    def remove_pin(self, pin):
        activity = pin.create_activity()
        # removes the pin from the user's followers feeds
        self.remove_user_activity(pin.user_id, activity)



    def follow(self,actor,target):
        activity=actor.Follow(target.user_id)
        self.add_user_activity(actor.user_id,activity)



    def get_user_follower_ids(self,user_id):
        query=self.session.query(UserRelation).filter(UserRelation.User2ID==user_id).all()
        follower_ids=[]
        for row in query:
            follower_ids.append(row.User1ID)
#        for follwer in follower_ids:
#            print follwer
        return {FanoutPriority.HIGH:follower_ids}

manager = PinManager()


testpin=Pin(id=1,user_id=1,item_id=18,message='testpin')
#user2=UserPinFeed(user_id=2)
#active=testpin.create_activity()

#feed.insert_activity(active)
#feed=PinFeed(1)
#feed.delete()
#feed2=PinFeed(2)
#feed.add(active)
#manager.follow_many_users(1,[2],False)
#manager.follow_user(2,1)
#feed.add(active)
#feed.flush()
#manager.batch_import(1,[active])


#print manager.get_user_follower_ids(1)
manager.add_pin(testpin)



#userpin=manager.get_feeds(2)['normal']
#actives=userpin['normal']
#print userpin[:10]

#print 'feed:', feed.count()
#print feed[:10]
#print 'feed2:', feed2.count()
#print feed2[:10]
#print userpin[:10]

#feed.delete()
#feed2.delete()

#
#
# userpin=User(1)
# targetpin=User(2)
#
# manager.add_pin(userpin)
# manager.add_pin(targetpin)
#
# userpin.Follow(2)

#userpin.Follow(3)
#manager.follow(userpin,targetpin)
#manager.follow_user(1,2)
# pic=Photos(Name='photo',
#     UID=1,
#     Description='new photo',
#     Path='\img\img1.jpg',
#     Filename='img1.jpg',
#     PAddDate='2015-1-1')
# manager.session.add(pic)
# manager.session.commit()
# print 'pic id',pic.ID
#
# userpin.add_pic(pic.ID)
# activaty=userpin.add_comment(pic.ID)
# manager.add_pin(userpin)
# manager.add_user_activity(1,activaty)
#
# feeds= manager.get_feeds(2)['normal']
#
# print feeds.count()
# print feeds[0]
# print 'userpin:',userpin[:100]
# print 'targetpin',targetpin[:100]
# manager.add_pin(userpin)
# manager.add_pin(targetpin)
# print manager.get_user_feed(2)[:]
#
# userpin.delete()
# targetpin.delete()

