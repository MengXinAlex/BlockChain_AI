from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','is_staff','is_buyer')

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('description', 'cover', 'image')
