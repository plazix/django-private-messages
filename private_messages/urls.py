# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *


urlpatterns = patterns('private_messages.views',
    url(r'^$', 'topics', name='private_messages'),
    url(r'^read/(?P<topic_id>[\d]+)/$', 'topic_read', name='private_messages_topic'),
    url(r'^new/$', 'topic_new', name='private_messages_new'),
    url(r'^delete/$', 'topic_delete', name='private_messages_topic_delete'),
)
