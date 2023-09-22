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
                queryset=CustomFormField.objects.none(),
                widget=forms.CheckboxSelectMultiple,
                required=False,
                initial=[],
    )

    def __init__(self, *args, project=None, **kwargs):
        super(TemplateBuilderForm, self).__init__(*args, **kwargs)
        if project:
            self.fields['agent_fields'].queryset = CustomFormField.objects.filter(project=project)

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
    
    def __init__(self, *args, project=None, **kwargs):
        super(TemplateEditForm, self).__init__(*args, **kwargs)
        if project:
            self.fields['agent_fields'].queryset = CustomFormField.objects.filter(project=project)

class AddProjectForm(forms.Form):
    name = forms.CharField(max_length=40)
    signature = forms.CharField(widget=forms.Textarea)

class EditSignatureForm(forms.Form):
    signature = forms.CharField(widget=forms.Textarea)

class FormCreatorForm(forms.Form):
    FIELD_TYPES = [
        ('ChoiceField', 'ChoiceField'),
        ('IntegerField', 'IntegerField'),
        ('CharField', 'CharField'),
        ('EmailField', 'EmailField'),
        ('TextField', 'TextField'),
        ('EKField', 'EKField'),
    ]

    label = forms.CharField(max_length=60, label='')
    field_type = forms.ChoiceField(choices=FIELD_TYPES, widget=forms.Select, label='')
    required = forms.BooleanField(initial=True, required=False, label='Required')
    choices = forms.CharField(max_length=200, required=False, widget=forms.Textarea, label='')

class FormDeleteForm(forms.Form):
    form_fields = forms.ModelMultipleChoiceField(
                queryset=CustomFormField.objects.none(),
                widget=forms.CheckboxSelectMultiple,
                required=False,
                initial=[],
                label='',
    )

    def __init__(self, *args, project=None, **kwargs):
        super(FormDeleteForm, self).__init__(*args, **kwargs)
        if project:
            self.fields['form_fields'].queryset = CustomFormField.objects.filter(project=project)