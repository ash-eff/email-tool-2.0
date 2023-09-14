from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import (ProjectSelectionForm, EmailTemplateForm)
from .models import Project, EmailTemplate, CustomFormTemplate
from django import forms

class ProjectSelectionView(View):
    def get(self, request):
        form = ProjectSelectionForm()
        return render(request, 'home.html', {'form': form})
    
    def post(self, request):
        form = ProjectSelectionForm(request.POST)
        if form.is_valid():
            selected_project = form.cleaned_data['project']
            return HttpResponseRedirect(reverse('project-landing-page', args=[selected_project]))
        else:
            # Handle the case where the form is not valid, e.g., re-render the form with errors
            return render(request, 'home.html', {'form': form}) 
        
class ProjectLandingPageView(View):
    def get(self, request, name):
        selected_project_name = name.upper()
        selected_project = get_object_or_404(Project, name=name)
        email_templates = selected_project.email_templates.all()
        return render(request, 'project-landing-page.html', {'selected_project': selected_project, 'email_templates': email_templates, 'selected_project_name': selected_project_name})
    
    def post(self, request, name):
        selected_project_name = name.upper()
        selected_project = get_object_or_404(Project, name=name)
        template_subject = request.POST.get('template_subject', None)
        selected_template = selected_project.email_templates.get(subject=template_subject)
        print(selected_template.template_text)
        return render(request, 'email-template.html', {'selected_project': selected_project, 'selected_template': selected_template, 'selected_project_name': selected_project_name})
    
class CreateEmailView(View):
    
    def get(self, request, name, email_subject):
        selected_project = get_object_or_404(Project, name=name)
        template = get_object_or_404(EmailTemplate, subject=email_subject)
        template_forms = template.custom_form_template

        form_fields = {}
        for field in template_forms.fields.all():
            field_name = field.label
            print(field_name)
            field_type = field.field_type
            field_choices = field.choices.split(',') if field.choices else []
            field_required = field.required

            if field_type == 'CharField':
                form_fields[field_name] = forms.CharField(
                    required=field_required,
                    label=field_name.title(),
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                )
            elif field_type == 'EmailField':
                form_fields[field_name] = forms.EmailField(
                    required=field_required,
                    label=field_name.title(),
                    widget=forms.EmailInput(attrs={'class': 'form-control'}),
                )
            elif field_type == 'ChoiceField':
                form_fields[field_name] = forms.ChoiceField(
                    choices=[(choice.strip(), choice.strip()) for choice in field_choices],
                    required=field_required,
                    label=field_name.title(),
                    widget=forms.Select(attrs={'class': 'form-control'}),
                )
            elif field_type == 'IntegerField':
                form_fields[field_name] = forms.IntegerField(
                    required=field_required,
                    label=field_name.title(),
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                )

        CustomEmailForm = type('CustomEmailForm', (forms.Form,), form_fields)
        form = CustomEmailForm
        #print('form: ' + str(form_fields))  
        return render(request, 'email-template.html', {'form': form})
    
    def post(self, request, name, email_subject):
        selected_project = get_object_or_404(Project, name=name)
        template = get_object_or_404(EmailTemplate, subject=email_subject)
        template_forms = template.custom_form_template

        form_fields = {}
        for field in template_forms.fields.all():
            field_name = field.label
            field_type = field.field_type
            field_choices = field.choices.split(',') if field.choices else []
            field_required = field.required

            if field_type == 'CharField':
                form_fields[field_name] = forms.CharField(
                    required=field_required,
                    label=field_name.title(),
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                )
            elif field_type == 'EmailField':
                form_fields[field_name] = forms.EmailField(
                    required=field_required,
                    label=field_name.title(),
                    widget=forms.EmailInput(attrs={'class': 'form-control'}),
                )
            elif field_type == 'ChoiceField':
                form_fields[field_name] = forms.ChoiceField(
                    choices=[(choice.strip(), choice.strip()) for choice in field_choices],
                    required=field_required,
                    label=field_name.title(),
                    widget=forms.Select(attrs={'class': 'form-control'}),
                )
            elif field_type == 'IntegerField':
                form_fields[field_name] = forms.IntegerField(
                    required=field_required,
                    label=field_name.title(),
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                )

        CustomEmailForm = type('CustomEmailForm', (forms.Form,), form_fields)
        form = CustomEmailForm(request.POST)
             

        if form.is_valid():
            template_text = template.template_text
            formatted_text = template_text.format(**form.cleaned_data)
            
            return render(request, 'email-template.html', {'form': form, 'formatted_text':  formatted_text,})
        else:
            return render(request, 'email-template.html', {'form': form})