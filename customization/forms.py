from django import forms
from .models import *


def create_setting_form(src_model):
    class ClienSettingForm(forms.ModelForm):
        required_css_class = 'required'

        class Meta:
            model = src_model
            exclude = ('status', 'created_at', 'updated_at',)

    return ClienSettingForm


def update_setting_form(src_model):
    class SettingUpdateForm(forms.ModelForm):
        required_css_class = 'required'

        class Meta:
            model = src_model
            exclude = ('created_at', 'updated_at',)

    return SettingUpdateForm
