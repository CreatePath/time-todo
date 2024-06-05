from django import forms
from django.contrib.auth.models import User

class AccountForm(forms.Form):
    username = forms.CharField(label="Id", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), max_length=64)
    password_verification = forms.CharField(label="Password Verification", widget=forms.PasswordInput(), max_length=64)
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label="Last Name", max_length=30)
    email = forms.CharField(label="Email", max_length=100)