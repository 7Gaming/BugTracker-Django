from django import forms
from .models import Bug

class SubmitBugForm(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        "placeholder": "Please name the bug."
    }))

    description = forms.CharField(widget=forms.Textarea(attrs={
        "rows": 3, 
        "cols": 30,
        "placeholder": "Please describe the bug."
    }))

class ChangeStatusForm(forms.Form):
    name = forms.CharField(max_length=30)
    status = forms.CharField(max_length=12)