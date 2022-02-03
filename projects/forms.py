from .models import Comment, Project, Update
from django import forms
from datetime import datetime
from datetime import timedelta

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('header', 'body')
        labels = {
            'header': "Title",
            'body': "Comment"
        }
        
class UpdateForm(forms.ModelForm):
    class Meta:
        model = Update
        fields = ('header', 'body')
        labels = {
            'header': "Title",
            'body': "Comment"
        }

class ProjectSuggestForm(forms.ModelForm):
    scale = forms.ChoiceField(label="Project Scale", choices=((None, 'Select Timescale'), ("shortterm", '1 week'), ("mediumterm", '1 month'), ("longterm", '3 months')))

    priceEstimate = forms.Field(required=False,disabled=True,label="Estimated Price to fund")

    def save(self, costDistribution, suggester, commit=True):
        instance = super(ProjectSuggestForm, self).save(commit=False)

        scale = self.cleaned_data["scale"]
        
        if (scale == "shortterm"):
           instance.expectedLength = timedelta(days=2*7)
        elif (scale == "midterm"):
           instance.expectedLength = timedelta(days=4*7)
        elif (scale == "longterm"):
           instance.expectedLength = timedelta(days=4*7*3)

        instance.approved = False
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

class DateInput(forms.DateInput):
    input_type = 'date'

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = []
        widgets = {
            'startDate': DateInput(),
            'endDate': DateInput(),
        }
