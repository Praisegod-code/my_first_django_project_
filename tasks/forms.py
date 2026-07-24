from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task

class TaskForm(forms.ModelForm):
    due_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Task
        fields = ('title', 'done', 'due_time')


class TaskCreateForm(forms.ModelForm):
    due_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Task
        fields = ('title', 'due_time')

class Registerform(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')