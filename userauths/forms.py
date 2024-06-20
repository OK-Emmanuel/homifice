from django import forms
from django.contrib.auth.forms import UserCreationForm

from userauths.models import User

class UserRegisterForm(UserCreationForm):
    
    # manupulate default form placeholder
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Full Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Email Address'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Create Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    
    
    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'phone', 'password1', 'password2']
