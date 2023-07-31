from django import forms
from .models import Student, Group
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordResetForm,
    PasswordChangeForm,
)
from django.contrib.auth.models import User


class StudentRegistrationForm(UserCreationForm):
    course = forms.ModelChoiceField(queryset=Group.objects.all())
    email = forms.EmailField(required=False)
    date_of_birth = forms.DateField(help_text="Required. Format: YYYY-MM-DD")
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    country = forms.CharField(max_length=255)
    picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "course",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "date_of_birth",
            "address",
            "city",
            "country",
            "picture",
        ]


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ("address", "city", "country", "picture")


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class CustomPasswordResetForm(PasswordResetForm):
    class Meta:
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control mt-3", "placeholder": "Enter email"}
            )
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email does not exist on our record.")
        return email


class CustomPasswordConfirmForm(PasswordChangeForm):
    pass
