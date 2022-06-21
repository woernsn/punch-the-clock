from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

from . import models


class ProfileForm(forms.Form):
    token = forms.CharField(label='API Token', disabled=True, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))


class TimeLogForm(forms.ModelForm):
    class Meta:
        model = models.TimeLog
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date > end_date:
            raise ValidationError(
                message='The start date has to be before the end date.', code='time_mismatch')


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control'}
        )
