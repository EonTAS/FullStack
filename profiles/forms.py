from .models import UserProfile
from django import forms

from django.contrib.auth.models import User

#form to update user info
class UserForm(forms.ModelForm):
    sendEmailUpdates = forms.BooleanField(required=False, label="Send Email when funded projects get updated")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        #allow default value of email notifications to read from userprofile
        if instance is not None:
            self.fields['sendEmailUpdates'].initial = instance.userprofile.email_updates

    def save(self, commit=True):
        instance = super(UserForm, self).save(commit=False)
        #autosave email updates setting 
        instance.userprofile.email_updates = self.cleaned_data["sendEmailUpdates"]
        
        if commit:
            instance.save()
        return instance