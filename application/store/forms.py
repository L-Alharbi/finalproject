from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User

# Create forms here

class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username','email'] 

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2'] 