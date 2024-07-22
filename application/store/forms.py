from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from django.contrib.auth.models import User
from .models import Review

# Create forms here

class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1','new_password2']


class UpdateUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','email'] 

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2'] 

class ReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "write review"}))

    class Meta:
        model = Review
        fields = ['review','rating']