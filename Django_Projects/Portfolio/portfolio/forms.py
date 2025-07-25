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

    email = forms.EmailField(
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Your Email'
        })
    )

    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Subject'
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Your Message',
            'rows': 5
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        # Add any custom validation here
        return cleaned_data