from django import forms
from django.core.validators import EmailValidator
from .models import Project

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Your Name'
        })
    )