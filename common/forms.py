from django import forms
from common.models import User

class SignUpForm(forms.Form):
    username = forms.CharField(label="Id", max_length=30)
    password = forms.CharField(label="Password", max_length=64)
    password_verification = forms.CharField(label="Password Verification", max_length=64)
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label="Last Name", max_length=30)
    email = forms.CharField(label="Email", max_length=100)
