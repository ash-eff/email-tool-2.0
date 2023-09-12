from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import (ProjectSelectionForm, EmailTemplateForm, TexasNoTideEmailTemplateForm, 
                    OhioNoTideEmailtemplateForm, MAAC2WashingtonNoTideTemplateForm, MAAC2IdahoNoTideTemplateForm, 
                    MAAC2HawaiiNoTideTemplateForm, ClearCacheAndCookiesForm)
from .models import Project

class ProjectSelectionView(View):
    def get(self, request):
        form = ProjectSelectionForm()
        return render(request, 'home.html', {'form': form})
    
    def post(self, request):
        form = ProjectSelectionForm(request.POST)
        if form.is_valid():
            selected_project = form.cleaned_data['project']
            return HttpResponseRedirect(reverse('project-landing-page', args=[selected_project]))  
        
class ProjectLandingPageView(View):
    def get(self, request, name):
        selected_project_name = name.upper()
        selected_project = get_object_or_404(Project, name=name)
        email_templates = selected_project.email_templates.all()
        return render(request, 'project-landing-page.html', {'selected_project': selected_project, 'email_templates': email_templates, 'selected_project_name': selected_project_name})
          
class NoTideEmailTemplateView(View):
    def get(self, request, name):
        selected_project = get_object_or_404(Project, name=name)
        selected_project_name = name.upper()
        match selected_project_name:
            case 'TEXAS':
                form_class = TexasNoTideEmailTemplateForm
            case 'OHIO':
                form_class = OhioNoTideEmailtemplateForm
            case 'MAAC2-WASHINGTON':
                form_class = MAAC2WashingtonNoTideTemplateForm
            case 'MAAC2-IDAHO':
                form_class = MAAC2IdahoNoTideTemplateForm
            case 'MAAC2-HAWAII':
                form_class = MAAC2HawaiiNoTideTemplateForm
            case _:
                form_class = EmailTemplateForm

        form = form_class
        return render(request, 'no-tide-email-template.html', {'form': form, 'name': name, 'selected_project': selected_project, 'selected_project_name': selected_project_name})
    
    def post(self, request, name):
        selected_project = get_object_or_404(Project, name=name)
        selected_project_name = name.upper()
        match selected_project_name:
            case 'TEXAS':
                form = TexasNoTideEmailTemplateForm(request.POST)
            case 'OHIO':
                form = OhioNoTideEmailtemplateForm(request.POST)
            case 'MAAC2-WASHINGTON':
                form = MAAC2WashingtonNoTideTemplateForm(request.POST)
            case 'MAAC2-IDAHO':
                form = MAAC2IdahoNoTideTemplateForm(request.POST)
            case 'MAAC2-HAWAII':
                form = MAAC2HawaiiNoTideTemplateForm(request.POST)
            case _:
                form = EmailTemplateForm(request.POST)

        if form.is_valid():
            selected_project = get_object_or_404(Project, name=name)
            subject_line = name.title() + ' No Tide'
            no_tide_template = selected_project.email_templates.get(subject=subject_line)
            template_text = no_tide_template.template_text
            formatted_text = template_text.format(**form.cleaned_data)
            return render(request, 'no-tide-email-template.html', {'form': form, 'formatted_text': formatted_text, 'selected_project': selected_project, 'selected_project_name': selected_project_name})
        
        return render(request, 'no-tide-email-template.html', {'form': form, 'selected_project': selected_project, 'selected_project_name': selected_project_name})

class ClearCacheAndCookiesView(View):
    def get(self, request, name):
        selected_project = get_object_or_404(Project, name=name)
        selected_project_name = name.upper()
        form = ClearCacheAndCookiesForm
        return render(request, 'clear-cache-and-cookies.html', {'form': form, 'selected_project': selected_project, 'selected_project_name': selected_project_name})
    
    def post(self, request, name):
        form = ClearCacheAndCookiesForm(request.POST)
        if form.is_valid():
            selected_project = get_object_or_404(Project, name=name)
            selected_project_name = name.upper()
            project = get_object_or_404(Project, name=selected_project)
            subject_line = name.title() + ' Clear Cache'
            clear_cache_email_template = project.email_templates.get(subject=subject_line)
            template_text = clear_cache_email_template.template_text
            formatted_text = template_text.format(**form.cleaned_data)
            return render(request, 'clear-cache-and-cookies.html', {'form': form, 'formatted_text': formatted_text, 'selected_project': selected_project, 'selected_project_name': selected_project_name})
        
        return render(request, 'clear-cache-and-cookies.html', {'form': form, })