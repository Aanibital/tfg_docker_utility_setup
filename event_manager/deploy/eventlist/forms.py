# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import EventList


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "Username",
            "class": "form-control"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder": "Password",
            "class": "form-control"
        }
    ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "Username",
            "class": "form-control"
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "placeholder": "Email",
            "class": "form-control"
        }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder": "Password",
            "class": "form-control"
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder": "Password check",
            "class": "form-control"
        }
    ))

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

class addListForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "Name",
            "class": "form-control"
        }
    ))

class addEventForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "Name",
            "class": "form-control",
        }
    ))

    date = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={
            "placeholder": "Date",
            "class": "form-control",
            "type": "datetime-local"
        }
    ))

    description = forms.CharField(required = False, widget=forms.TextInput(
        attrs={
            "placeholder": "Description",
            "class": "form-control",
        }
    ))

class EditListForm(forms.ModelForm):
    model = EventList
    fields = ['name', 'users']
