# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from conf import settings


class TopicManager(models.Manager):
    def by_user(self, user):
        """
        Все топики выбранного пользователя
        """
        return self.filter(models.Q(sender=user) | models.Q(recipient=user))


class MessageManager(models.Manager):
    def count_unread(self, user, topic=None):
        """
        Количество непрочитанных сообщений
        """
        qs = self.filter(models.Q(topic__recipient=user) | models.Q(topic__sender=user), read_at__exact=None).\
                exclude(sender=user)
        if topic is not None:
            qs = qs.filter(topic=topic)
        return qs.count()

    def by_topic(self, topic):
        """
        Все сообщение в топике
        """
        return self.select_related('sender').filter(topic=topic)

    def mark_read(self, user, topic):
        """
        Помечаем сообщения как прочитанные
        """
        self.exclude(sender=user).filter(topic=topic, read_at__exact=None).update(read_at=datetime.now())


class Topic(models.Model):
    sender = models.ForeignKey(settings.USER_MODEL, verbose_name=_('Sender'), related_name='pm_topics_sender')
    recipient = models.ForeignKey(settings.USER_MODEL, verbose_name=_('Recipient'), related_name='pm_topics_recipient')
    subject = models.CharField(_('Subject'), max_length=255)
    last_sent_at = models.DateTimeField()

    objects = TopicManager()

    class Meta:
        ordering = ['-last_sent_at']

    def __unicode__(self):
        return self.subject

    @models.permalink
    def get_absolute_url(self):
        return 'private_messages_topic', [self.pk]

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
    sender = models.ForeignKey(settings.USER_MODEL, verbose_name=_('Sender'))
    body = models.TextField(_('Message'))
    sent_at = models.DateTimeField(_('Posted'), auto_now_add=True)
    read_at = models.DateTimeField(_('Read'), blank=True, null=True, default=None)

    objects = MessageManager()

    class Meta:
        ordering = ['-sent_at']

    def get_absolute_url(self):
        return '%s#message-%s' % (self.topic.get_absolute_url(), self.pk)
