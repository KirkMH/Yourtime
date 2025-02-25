from django import forms

from .models import *
from access.models import Employee


class WatchForm(forms.ModelForm):
    required_css_class = 'required'

    BOOLEAN_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]

    class Meta:
        model = Watch
        exclude = ('owner', )

    def __init__(self, *args, **kwargs):
        super(WatchForm, self).__init__(*args, **kwargs)
        self.fields['with_card'] = forms.ChoiceField(
            label="With Guarantee/Warranty Card?",
            choices=self.BOOLEAN_CHOICES,
            required=True,
            widget=forms.Select
        )
        self.fields['for_him'] = forms.ChoiceField(
            label="For Him?",
            choices=self.BOOLEAN_CHOICES,
            required=True,
            widget=forms.Select
        )
        self.fields['for_her'] = forms.ChoiceField(
            label="For Her?",
            choices=self.BOOLEAN_CHOICES,
            required=True,
            widget=forms.Select
        )


class JobOrderForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = JobOrder
        fields = ['repair_work', 'external_case_and_bracelet', 'notices', 'condition', 'warranty',
                  'warranty_file_1', 'warranty_file_2', 'warranty_file_3',
                  'assigned_technician', 'current_status', 'promise_date']

    def __init__(self, *args, **kwargs):
        super(JobOrderForm, self).__init__(*args, **kwargs)
        self.fields['repair_work'].widget = forms.TextInput()
        self.fields['external_case_and_bracelet'].widget = forms.TextInput()
        self.fields['warranty'].widget = forms.TextInput()
        self.fields['assigned_technician'].queryset = Employee.technicians.filter(
            is_active=True)


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


class ArrivalPhotoForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = ArrivalPhoto
        fields = ['photo']


class ReleasePhotoForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = ReleasePhoto
        fields = ['photo']


class PaymentForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Payment
        exclude = ['job_order', 'received_by', ]
