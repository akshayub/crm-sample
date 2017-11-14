from django import forms
from django.contrib.auth.models import User
from objects.models import *
from django.views.generic.edit import UpdateView


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


class LeadForm(forms.ModelForm):

    class Meta:
        model = Lead
        fields = ['name', 'address', 'email', 'company', 'amount']


class OppoForm(forms.ModelForm):

    class Meta:
        model = Opportunity
        fields = ['name', 'amount', 'account', 'close_date', 'description']


class AccountUpdate(UpdateView):
    model = Account
    fields = ['name', 'website', 'phone_number', 'subsidiary_of']
    template_name_suffix = '_update_form'


class ContactUpdate(UpdateView):
    model = Contact
    fields = ['name', 'phone_number', 'email', 'address', 'bdate', 'works_for']
    template_name_suffix = '_update_form'


class LeadUpdate(UpdateView):
    model = Lead
    fields = ['name', 'address', 'email', 'company', 'amount']
    template_name_suffix = '_update_form'


class OppoUpdate(UpdateView):
    model = Opportunity
    fields = ['name', 'amount', 'account', 'close_date', 'description']
    template_name_suffix = '_update_form'
