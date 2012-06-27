# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from models import Message


class MessageSendForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('body',)


class NewTopicForm(MessageSendForm):
    recipient = forms.CharField(label=_('Recipient'), help_text=_('Specify the username'))
    subject = forms.CharField(label=_('Subject'))

    def clean_recipient(self):
        try:
            recipient = User.objects.get(username=self.cleaned_data['recipient'])
        except User.DoesNotExist:
            raise forms.ValidationError(_('Username not found'))

        return recipient
