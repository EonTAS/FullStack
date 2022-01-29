from .models import UserProfile
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('header', 'body')
        labels = {
        }
        