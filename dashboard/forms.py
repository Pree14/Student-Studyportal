from django import forms
from django.forms import widgets
from . models import *
from django.contrib.auth.forms import UserCreationForm

class NotesForm(forms.ModelForm):
    class Meta:  # no need to assign 3 clos just map it with models
        model = Notes
        fields = ['title','description']

class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm): # inherition
    class Meta:
        model = Homework
        widgets = {'due':DateInput()}
        fields = ['subject','title','description','due','is_finished'] #isfinished is a boolean value check or uncheck

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label="Enter your search  ")

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']

class UserRegistrationForm(UserCreationForm): # this will inherit to usercreation form section
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']