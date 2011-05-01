# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

from models import Message


class MessageSendForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('body',)


class NewTopicForm(MessageSendForm):
    recipient = forms.CharField(label=u'Кому', help_text=u'Укажите имя пользователя')
    subject = forms.CharField(label=u'Тема')

    def clean_recipient(self):
        try:
            recipient = User.objects.get(username=self.cleaned_data['recipient'])
        except User.DoesNotExist:
            raise forms.ValidationError(u'Пользователь с таким именем не найден')

        return recipient
