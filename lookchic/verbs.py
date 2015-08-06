# -*- coding: utf-8 -*-
from stream_framework.verbs import register
from stream_framework.verbs.base import Verb, Follow, Love


class Pin(Verb):
    id = 5
    infinitive = 'pin'
    past_tense = 'pinned'

register(Pin)


class AddPhoto(Verb):
    id=6
    infinitive = 'add'
    past_tense='added'

register(AddPhoto)