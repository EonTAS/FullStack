from .models import Comment, Project
from django import forms
from django.utils.translation import ugettext_lazy
from datetime import datetime
from datetime import timedelta

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('header', 'body')
        labels = {
            'header': "Title",
            'body': "Comment",
            'duration': "duration"
        }
        

class ProjectForm(forms.ModelForm):
    scale = forms.ChoiceField(label="Project Scale", choices=((None, 'Select Timescale'), ("shortterm", '1 week'), ("mediumterm", '1 month'), ("longterm", '3 months')))


    priceEstimate = forms.Field(required=False,disabled=True,label="Estimated Price to fund")

    def save(self, costDistribution, suggester, commit=True):
        instance = super(ProjectForm, self).save(commit=False)
        instance.startDate = datetime.now()
        scale = self.cleaned_data["scale"]
        if (scale == "shortterm"):
            instance.endDate = instance.startDate+timedelta(weeks=2)
        elif (scale == "midterm"):
            instance.endDate = instance.startDate+timedelta(months=1)
        elif (scale == "longterm"):
            instance.endDate = instance.startDate+timedelta(months=3)

        instance.price = costDistribution[str(scale) + " " + str(instance.category)]
        instance.suggester = suggester
  
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Project
        fields = ('name', 'category', 'description', 'image')
        labels = {'name': "Project Title"}
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Enter a succint name for your suggestion'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Describe in as much detail as possible what you want from the project'}),
        }
    
    field_order = ['name', 'category', 'scale', 'priceEstimate', 'description', 'image']