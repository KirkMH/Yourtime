from django import forms

from .models import *


class WatchForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Watch
        exclude = ('owner', )


class JobOrderForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = JobOrder
        fields = ['repair_work', 'external_case_and_bracelet', 'notices', 'condition', 'warranty',
                  'assigned_technician', 'current_status', 'promise_date']


class AssessmentForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Assessment
        fields = ['assessment', 'assessed_by', 'assessment_date']


class TestLogForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = TestLog
        exclude = ('job_order', 'encoded_at', )


class ChargeForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Charge
        exclude = ('job_order', )
