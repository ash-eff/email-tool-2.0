from django import forms
from django.db import models
from django.forms import ModelForm
from .models import CustomFormField, Project
from django.db.models import Q


class ProjectSelectionForm(forms.Form):
    project = forms.ChoiceField(required=True, label='', 
                                widget=forms.Select(attrs={'class': 'form-control'}),)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        projects = Project.objects.filter(global_project=False)
        project_choices = [(project.id, project.name) for project in projects]
        self.fields['project'].choices = [('', 'Select a Project')] + project_choices

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

class SuperSecretForm(forms.Form):
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

class TemplateBuilderForm(forms.Form):
    template_name = forms.CharField(max_length=100)
    template = forms.CharField(widget=forms.Textarea)
    formatted_template = forms.CharField(required=False, widget=forms.Textarea)
    agent_fields = forms.ModelMultipleChoiceField(
                queryset=CustomFormField.objects.all(),
                widget=forms.CheckboxSelectMultiple,
                required=False,
                initial=[],
    )