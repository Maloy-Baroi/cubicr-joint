from django.contrib.auth.forms import UserCreationForm
from django import forms
from App_auth.models import *


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2',)


class ProfileModelForm(forms.ModelForm):
    Date_of_Birth = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    fullName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Mobile Number(example: +8801855279...'}))
    house_no = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'House No.'}))
    area = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Area'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City'}))

    class Meta:
        model = Profile_main
        exclude = ['user', ]


class SkillListModelForm(forms.ModelForm):
    class Meta:
        model = SkillListModel
        exclude = ['user']


class EducationModelForm(forms.ModelForm):
    starting_year = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    passing_year = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'required': 'false'}))

    class Meta:
        model = EducationModel
        exclude = ['user', 'active']


class Extra_curricular_Activities_ModelForm(forms.ModelForm):
    perform_time = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Extra_curricular_Activities_Model
        exclude = ['user']


class Co_curricular_Activities_ModelForm(forms.ModelForm):
    perform_time = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Co_curricular_Activities_Model
        exclude = ['user']


class ExperiencesModelForm(forms.ModelForm):
    starting_year = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    leaving_year = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = ExperiencesModel
        exclude = ['user']


class ReferencesModelForm(forms.ModelForm):
    name_of_reference = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name of Reference'}))
    position = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'example: Professor'}))
    contact = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'example: +880185527....'}))

    class Meta:
        model = ReferencesModel
        exclude = ['user', 'created']
