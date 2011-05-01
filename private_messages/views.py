# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from models import Topic, Message
from forms import NewTopicForm, MessageSendForm


@login_required
def topics(request, template_name='private_messages/topics.html'):
    return TemplateResponse(request, template_name, {
        'pm_topics': Topic.objects.by_user(request.user)
    })


@login_required
def topic_new(request, template_name='private_messages/topic_new.html'):
    if request.method == 'POST':
        form = NewTopicForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)

            topic = Topic(sender=request.user)
            topic.recipient = form.cleaned_data['recipient']
            topic.subject = form.cleaned_data['subject']
            topic.last_sent_at = datetime.now()
            topic.save()

            message.topic = topic
            message.sender = request.user
            message.save()

            return HttpResponseRedirect(topic.get_absolute_url())
    else:
        initial = {}
        if request.GET.has_key('recipient'):
            initial['recipient'] = request.GET['recipient']

        form = NewTopicForm(initial=initial)

    return TemplateResponse(request, template_name, {
        'pm_form': form,
    })


@login_required
def topic_read(request, topic_id, template_name='private_messages/topic_read.html'):
    topic = get_object_or_404(Topic.objects.by_user(request.user), id=topic_id)

    if request.method == 'POST':
        form = MessageSendForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.topic = topic
            message.sender = request.user
            message.save()

            topic.last_sent_at = message.sent_at
            topic.save()

            return HttpResponseRedirect(message.get_absolute_url())
    else:
        form = MessageSendForm()

    # помечаем сообщения как прочитанные
    Message.objects.mark_read(request.user, topic)

    return TemplateResponse(request, template_name, {
        'pm_topic': topic,
        'pm_form': form,
    })


@login_required
def topic_delete(request):
    topics = []
    if request.method == 'POST':
        topics = request.POST.getlist('topic[]')
    elif request.GET.has_key('topic_id'):
        topics.append(request.GET['topic_id'])

    for topic_id in topics:
        try:
            topic = Topic.objects.by_user(request.user).get(pk=topic_id)
            topic.delete()
        except Topic.DoesNotExist:
            pass

    return HttpResponseRedirect(reverse('private_messages'))
