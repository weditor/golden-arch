# -*- encoding: utf-8 -*-
from django import forms
from .models import Conference, ConferenceTopic


class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ("id", "name", "description", "holding_time")


class ConferenceTopicForm(forms.ModelForm):
    class Meta:
        model = ConferenceTopic
        fields = "__all__"
        exclude = ("creator", )

