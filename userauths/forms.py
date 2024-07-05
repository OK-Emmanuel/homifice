from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User
from userauths.models import Profile
from django.forms import FileInput

class UserRegisterForm(UserCreationForm):
    
    # manupulate default form placeholder
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Full Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Email Address'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Create Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    
    # Specify the model and fields to include in the form
    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'phone', 'password1', 'password2']


# User update form
class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields= ['email']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "image",
            "full_name",
            "phone",
            "gender",
            "country",
            "city",
            "state",
            "address",
            "identity_type",
            "identity_image",
            "facebook",
            "twitter",
        ]

        widgets = {
            'image': FileInput(attrs={"onchange":"loadFile(event)", "class":"upload" }),
        }