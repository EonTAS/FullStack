from .models import Comment
from django import forms
from django.utils.translation import ugettext_lazy

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('header', 'body',)
        labels = {
            'header': "Title",
            'body': "Comment"
        }