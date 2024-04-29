from django import forms
from .models import userTypes


class NewEmployeeForm(forms.Form):
    required_css_class = 'required'

    username = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    user_type = forms.ChoiceField(choices=userTypes, required=True)


class UpdateEmployeeForm(forms.Form):
    required_css_class = 'required'

    username = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
