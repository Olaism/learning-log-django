from django import forms

from .models import (
    Subject,
    Topic,
    Entry
)

class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ['name', 'code', 'detail']

class TopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ['topic']

class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
