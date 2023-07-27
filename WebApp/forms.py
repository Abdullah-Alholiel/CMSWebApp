from django import forms


class YoutubeForm(forms.Form):
    text = forms.CharField(max_length=100,label="Enter Your search ")
