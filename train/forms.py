from django import forms
from django.contrib.auth.models import User


class AuthForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class ReviewForm(forms.Form):
	rating = forms.IntegerField()
	feedback = forms.CharField(max_length=500, widget=forms.Textarea)
