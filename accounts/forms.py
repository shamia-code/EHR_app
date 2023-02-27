# Creating a forms.py file in the accounts app that inherits from the Form class
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65, help_text="Patient Number or Professional Licence Number")
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

    class Meta:
        labels = {
            "username": "Patient/Professional Licence Number"
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
        labels = {
            "username": "Professional Licence Number"
        }
