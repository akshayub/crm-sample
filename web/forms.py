from django import forms
from django.contrib.auth.models import User
from objects.models import *


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['name', 'website', 'phone_number', 'subsidiary_of']


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'email', 'address', 'bdate', 'works_for']
