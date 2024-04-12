from django import forms

from .models import Watch


class WatchForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Watch
        exclude = ('owner', )
