from django import forms
from .models import *


############################
#       CLIENT
############################
class ClientForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Client
        exclude = ('is_active', 'created_at', 'updated_at',)


class ClientUpdateForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Client
        exclude = ('created_at', 'updated_at',)


class InquiryForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Inquiry
        exclude = ('created_at',)
