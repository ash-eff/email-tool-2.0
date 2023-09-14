from django import forms
from django.db import models
from django.forms import ModelForm

PROJECT_CHOICES = [
    ('indiana', 'Indiana'),
    ('maac2-hawaii', 'MAAC2 - Hawaii'), 
    ('maac2-idaho', 'MAAC2 - Idaho'), 
    ('maac2-washington', 'MAAC2 - Washington'), 
    ('ohio', 'Ohio'),
    ('texas', 'Texas'),
]

class ProjectSelectionForm(forms.Form):
    project = forms.ChoiceField(choices=PROJECT_CHOICES, required=True, label='', 
                                widget=forms.Select(attrs={'class': 'form-control'}),)

class EmailTemplateForm(forms.Form):
    greeting_choices = [
        ('Hello', 'Hello'),
        ('Greetings', 'Greetings'),
        ('Good Morning', 'Good Morning'),
        ('Good Afternoon', 'Good Afternoon'),
        ('Good Evening', 'Good Evening'),
    ]

    closing_choices = [
        ('Thank you', 'Thank you'),
        ('Best Regards', 'Best Regards'),
        ('Regards', 'Regards'),
    ]

    greeting = forms.ChoiceField(choices=greeting_choices, required=True, label='Greeting')
    closing = forms.ChoiceField(choices=closing_choices, required=True, label="Closing")
    user_name = forms.CharField(max_length=100, required=True, label="User's Full Name")
    case_number = forms.IntegerField(required=True, label="Case Number")
    agent_name = forms.CharField(max_length=1200, required=True, label="Agent's Name (first name and last initial)")

