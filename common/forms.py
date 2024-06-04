from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    username = forms.CharField(label="Id", max_length=30)
    password = forms.CharField(label="Password", max_length=64)
    password_verification = forms.CharField(label="Password Verification", max_length=64)
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label="Last Name", max_length=30)
    email = forms.CharField(label="Email", max_length=100)



class AccountUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text="비밀번호를 변경하려면 입력하세요.")
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
        }