from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django import forms

class RegistrationForm(UserCreationForm):
	height = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control'}))
	weight = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control'}))
	age = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ['username','email','height','weight','age','password1','password2']
		widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
        }

class LoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	class Meta:
		model = AuthenticationForm
		fields = ['username','password']

