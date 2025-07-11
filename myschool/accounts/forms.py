from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('parent', 'Parent'), 
        ('teacher', 'Teacher'),
        ('director', 'Director'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Роль', widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role')