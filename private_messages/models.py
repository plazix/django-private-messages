# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class TopicManager(models.Manager):
#    def get_query_set(self):
#        # todo стоит ли так делать?
#        return self.select_related('sender', 'recipient')

    def by_user(self, user):
        '''
        Все топики выбранного пользователя
        '''
        return self.filter(models.Q(sender=user) | models.Q(recipient=user))


class MessageManager(models.Manager):
    def count_unread(self, user, topic=None):
        '''
        Количество непрочитанных сообщений
        '''
        qs = self.filter(models.Q(topic__recipient=user) | models.Q(topic__sender=user), read_at__exact=None).\
                exclude(sender=user)
        if topic is not None:
            qs = qs.filter(topic=topic)
        return qs.count()

    def by_topic(self, topic):
        '''
        Все сообщение в топике
        '''
        return self.select_related('sender').filter(topic=topic)

    def mark_read(self, user, topic):
        '''
        Помечаем сообщения как прочитанные
        '''
        self.exclude(sender=user).filter(topic=topic, read_at__exact=None).update(read_at=datetime.now())


class Topic(models.Model):
    sender = models.ForeignKey(User, verbose_name=u'Отправитель', related_name='pm_topics_sender')
    recipient = models.ForeignKey(User, verbose_name=u'Получатель', related_name='pm_topics_recipient')
    subject = models.CharField(u'Тема', max_length=255)
    last_sent_at = models.DateTimeField()

    objects = TopicManager()

    class Meta:
        ordering = ['-last_sent_at']

    def __unicode__(self):
        return self.subject

    @models.permalink
    def get_absolute_url(self):
        return ('private_messages_topic', [self.pk])

    def count_messages(self):
        return self.messages.count()

    def count_unread_messages(self):
        return self.messages.filter(read_at__exact=None).count()

    def last_unread_message(self):
        try:
            return self.messages.order_by('-sent_at').filter(read_at__exact=None)[0]
        except IndexError:
            return None


class Message(models.Model):
    topic = models.ForeignKey(Topic, related_name='messages')
    sender = models.ForeignKey(User, verbose_name=u'Автор')
    body = models.TextField(u'Сообщение')
    sent_at = models.DateTimeField(u'Отправлено', auto_now_add=True)
    read_at = models.DateTimeField(u'Прочитано', blank=True, null=True, default=None)

    objects = MessageManager()

    class Meta:
        ordering = ['-sent_at']

    def get_absolute_url(self):
        return '%s#message-%s' % (self.topic.get_absolute_url(), self.pk)
