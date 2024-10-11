# forms.py
from django import forms

class EventCompletionForm(forms.Form):
    completed = forms.BooleanField(required=False, label='Mark as Completed')
