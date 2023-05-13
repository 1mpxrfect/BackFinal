from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractUser
from django.forms import ModelForm
from .models import Products
from django.db import models


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use!!!")
        return email


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'description', 'price', 'category', 'picture']


class ProductMediaForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ["picture"]


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
