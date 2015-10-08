# -*- coding: utf-8 -*-
from stream_framework.aggregators.base import RecentVerbAggregator
from stream_framework.feeds.redis import RedisFeed
from stream_framework.feeds.aggregated_feed.redis import RedisAggregatedFeed
from stream_framework.activity import Activity
from stream_framework.verbs.base import Follow as verbFollow,Add,Love,Comment

class PinFeed(RedisFeed):
    key_format = 'feed:normal:%(user_id)s'


class AggregatedPinFeed(RedisAggregatedFeed):
    aggregator_class = RecentVerbAggregator
    key_format = 'feed:aggregated:%(user_id)s'


class UserPinFeed(PinFeed):
    key_format = 'feed:user:%(user_id)s'

class User(UserPinFeed):

    def add_pic(self, pic_id):
        activity=Activity(
            self.user_id,
            Add,
            pic_id,
            self.user_id,
            time=None
        )
        return activity


    def create_pic(self,pic_id):
        self.pic_id=pic_id

    def create_user(self,id,name):
        self.user_id=id
        self.name=name
        return self

    def create_comment(self,id,pic_id):
        self.comment_id=id

    def get_user_id(self):
        return self.user_id

    def Follow(self, target_id):
        activity=Activity(
            self.user_id,
            verbFollow,
            target_id
        )
        return activity

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

    def add_pic(self,pic_id):
        from stream_framework.activity import Activity
        from stream_framework.verbs.base import Follow,Add,Love,Comment
        return Activity(self.user_id,Add,pic_id)




    def Follow(self,target_id):
        return Activity(self.user_id, verbFollow,target_id)

    def add_comment(self,pic_id):
        comment=Comment()
        return Activity(self.user_id,Comment, comment, target=pic_id)

