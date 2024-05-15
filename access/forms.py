from django import forms
from .models import userTypes


class NewEmployeeForm(forms.Form):
    required_css_class = 'required'

    username = forms.CharField(max_length=100, required=False,
                               help_text="Leave blank if this employee is a non-user.")
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    user_type = forms.ChoiceField(choices=userTypes, required=True)


class UpdateEmployeeForm(forms.Form):
    required_css_class = 'required'

    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    password = forms.CharField(
        widget=forms.PasswordInput,
        max_length=100,
        required=False)
    retype_password = forms.CharField(
        widget=forms.PasswordInput,
        max_length=100,
        required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        retype_password = cleaned_data.get('retype_password')

        if password != retype_password:
            self.add_error('retype_password',
                           "Password and Retype password must match.")
