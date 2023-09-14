from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import (ProjectSelectionForm,)
from .models import Project, CustomFormTemplate
from django import forms
from django.core.exceptions import ValidationError
import re

class ProjectSelectionView(View):
    def get(self, request):
        form = ProjectSelectionForm()
        selected_project = None  # Set selected_project to None for this view
        return render(request, 'home.html', {'form': form, 'selected_project': selected_project})
    
    def post(self, request):
        form = ProjectSelectionForm(request.POST)
        if form.is_valid():
            selected_project = form.cleaned_data['project'].lower()
            return HttpResponseRedirect(reverse('project-landing-page', args=[selected_project]))
        else:
            # Handle the case where the form is not valid, e.g., re-render the form with errors
            return render(request, 'home.html', {'form': form}) 
        
class ProjectLandingPageView(View):
    def get(self, request, name):
        selected_project_name = name.title()
        selected_project = get_object_or_404(Project, name=selected_project_name)
        email_templates = selected_project.email_templates.all()
        return render(request, 'project-landing-page.html', {
            'selected_project': selected_project, 
            'email_templates': email_templates, 
            'selected_project_name': selected_project_name})
    
    def post(self, request, name):
        template_name = request.POST.get('template_name', None)
        return HttpResponseRedirect(reverse('email-template', args=[name, template_name]))
     
class CreateEmailView(View):
    def get(self, request, name, template_name):
        selected_project_name = name.upper()
        selected_project = get_object_or_404(Project, name=name)
        try:
            template = get_object_or_404(CustomFormTemplate, project_name=name.lower(), template_name=template_name)
        except CustomFormTemplate.DoesNotExist:
            # Handle the case where the template does not exist
            template = None

        field_order_config = template.field_order_config
        form_fields = {}
        sorted_fields = sorted(template.fields.all(), key=lambda field: field_order_config.get(f"{field.label} {field.label_two}" if field.label_two else field.label, 0))
        for field in sorted_fields:
            con_field_name = field.label + ' ' + field.label_two if field.label_two is not None else field.label
            field_name = con_field_name
            field_type = field.field_type
            field_choices = field.choices.split(',') if field.choices else []
            field_required = field.required

            if field_type == 'CharField':
                form_fields[con_field_name] = forms.CharField(
                    required=field_required,
                    label = con_field_name,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                )
            elif field_type == 'EmailField':
                form_fields[con_field_name] = forms.EmailField(
                    required=field_required,
                    label = con_field_name,
                    widget=forms.EmailInput(attrs={'class': 'form-control'}),
                )
            elif field_type == 'ChoiceField':
                form_fields[con_field_name] = forms.ChoiceField(
                    choices=[(choice.strip(), choice.strip()) for choice in field_choices],
                    required=field_required,
                    label = con_field_name,
                    widget=forms.Select(attrs={'class': 'form-control'}),
                )
            elif field_type == 'IntegerField':
                form_fields[con_field_name] = forms.IntegerField(
                    required=field_required,
                    label = con_field_name,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                )
            elif field_type == 'EKField':
                form_fields[con_field_name] = forms.IntegerField(
                    required=field_required,
                    label = con_field_name,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    validators=[self.validate_ekfield]
                )
            elif field_type == 'TextField':
                form_fields[con_field_name] = forms.CharField(
                    required=field_required,
                    label = con_field_name,
                    widget=forms.Textarea(attrs={'class': 'form-control'}),
                )
        CustomEmailForm = type('CustomEmailForm', (forms.Form,), form_fields)
        form = CustomEmailForm
        return render(request, 'email-template.html', {'form': form, 'selected_project': selected_project, 'selected_project_name': selected_project_name})
    
    def post(self, request, name, template_name):
        selected_project_name = name.upper()
        selected_project = get_object_or_404(Project, name=name)
        try:
            template = get_object_or_404(CustomFormTemplate, project_name=name.lower(), template_name=template_name)
        except CustomFormTemplate.DoesNotExist:
            # Handle the case where the template does not exist
            template = None
        template_forms = template.template_text

        field_order_config = template.field_order_config
        form_fields = {}
        sorted_fields = sorted(template.fields.all(), key=lambda field: field_order_config.get(f"{field.label} {field.label_two}" if field.label_two else field.label, 0))
        for field in sorted_fields:
            con_field_name = field.label + ' ' + field.label_two if field.label_two is not None else field.label
            field_name = field.label
            field_type = field.field_type
            field_choices = field.choices.split(',') if field.choices else []
            field_required = field.required

            if field_type == 'CharField':
                form_fields[con_field_name] = forms.CharField(
                    required=field_required,
                    label = con_field_name,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                )
            elif field_type == 'EmailField':
                form_fields[con_field_name] = forms.EmailField(
                    required=field_required,
                    label = con_field_name,
                    widget=forms.EmailInput(attrs={'class': 'form-control'}),
                )
            elif field_type == 'ChoiceField':
                form_fields[con_field_name] = forms.ChoiceField(
                    choices=[(choice.strip(), choice.strip()) for choice in field_choices],
                    required=field_required,
                    label = con_field_name,
                    widget=forms.Select(attrs={'class': 'form-control'}),
                )
            elif field_type == 'IntegerField':
                form_fields[con_field_name] = forms.IntegerField(
                    required=field_required,
                    label = con_field_name,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                )
            elif field_type == 'EKField':
                form_fields[con_field_name] = forms.IntegerField(
                    required=field_required,
                    label = con_field_name,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    validators=[self.validate_ekfield]
                )
            elif field_type == 'TextField':
                form_fields[con_field_name] = forms.CharField(
                    required=field_required,
                    label = con_field_name,
                    widget=forms.Textarea(attrs={'class': 'form-control'}),
                )
        
        CustomEmailForm = type('CustomEmailForm', (forms.Form,), form_fields)
        form = CustomEmailForm(request.POST)
             

        if form.is_valid():
            template_text = template.template_text
            form_data = form.cleaned_data.copy()
            result_id = form.data.get('Results ID', '')
            formatted_results = 'RID: ' + ', RID: '.join([value.strip() for value in re.split(r'[ ,]+', result_id)])
            form_data['Results ID'] = formatted_results

            formatted_text = template_text.format(**form_data)

            return render(request, 'email-template.html', {'form': form, 'formatted_text':  formatted_text, 'selected_project': selected_project, 'selected_project_name': selected_project_name})
        else:
            return render(request, 'email-template.html', {'form': form})
        
    def validate_ekfield(self, value):
        if value is not None and (value < 0 or value > 99999999):
            raise ValidationError('Must be a valid EK Number. Make sure you are not providing a Student Id!')