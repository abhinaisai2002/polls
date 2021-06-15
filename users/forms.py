from django import forms
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import models
from django.forms import fields

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username','password']

class ProfileForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['username','email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
