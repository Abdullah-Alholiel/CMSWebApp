from django import forms
from .models import Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False)
    date_of_birth = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    country = forms.CharField(max_length=255)
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth', 'address', 'city', 'country', 'photo']

class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField()

    class Meta:

        model = User

        fields = ['first_name', 'last_name', 'email']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

