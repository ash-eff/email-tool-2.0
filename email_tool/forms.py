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

class TemplateEditForm(forms.Form):
    template_name = forms.CharField(max_length=100)
    template = forms.CharField(widget=forms.Textarea)
    formatted_template = forms.CharField(required=False, widget=forms.Textarea)
    agent_fields = forms.ModelMultipleChoiceField(
                queryset=CustomFormField.objects.all(),
                widget=forms.CheckboxSelectMultiple,
                required=False,
                initial=[],
    )

class AddProjectForm(forms.Form):
    name = forms.CharField(max_length=40)
    signature = forms.CharField(widget=forms.Textarea)

class EditSignatureForm(forms.Form):
    signature = forms.CharField(widget=forms.Textarea)