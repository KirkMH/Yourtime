from django import forms

from .models import Watch, JobOrder


class WatchForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Watch
        exclude = ('owner', )


class JobOrderForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = JobOrder
        fields = ['repair_work', 'item_condition',
                  'assigned_technician', 'promise_date']
