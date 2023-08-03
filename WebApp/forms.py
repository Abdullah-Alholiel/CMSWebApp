from django import forms
from django import forms
from .models import Registration

class YoutubeForm(forms.Form):
    text = forms.CharField(max_length=100,label="Enter Your search ")

class BookForm(forms.Form):
    text = forms.CharField(max_length=100,label="Enter Your search ")



class ModuleRegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = []

class ModuleUnregistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = []
