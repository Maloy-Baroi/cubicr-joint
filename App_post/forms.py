from django import forms
from App_post.models import *


class JobPostModelForm(forms.ModelForm):
    application_deadline = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = JobPostModel
        exclude = ['author', 'status']


class PartnerRequestModelForm(forms.ModelForm):
    application_deadline = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = PartnerRequestModel
        exclude = ['author', 'status']


class JobApplyForm(forms.ModelForm):
    class Meta:
        model = JobApplicationModel
        exclude = ['candidate', 'status', 'applied_job']
