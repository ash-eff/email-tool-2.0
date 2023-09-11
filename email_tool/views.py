from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import (NoTideAccountForm, EmailTemplateForm, TexasNoTideEmailTemplateForm, 
                    OhioNoTideEmailtemplateForm, MAAC2WashingtonNoTideTemplateForm, MAAC2IdahoNoTideTemplateForm, 
                    MAAC2HawaiiNoTideTemplateForm, ClearCacheAndCookiesForm)
from .models import EmailTemplate, Project

def home_page(request):
    return render(request, 'index.html')

class NoTideAccountView(View):
    def get(self, request):
        form = NoTideAccountForm()
        return render(request, 'no-tide-account.html', {'form': form})
    
    def post(self, request):
        form = NoTideAccountForm(request.POST)
        if form.is_valid():
            selected_project = form.cleaned_data['project']
            return HttpResponseRedirect(reverse('no-tide-email-form-template', args=[selected_project]))  
          
class NoTideEmailTemplateView(View):
    def get(self, request, name):
        selected_project = name

        match selected_project:
            case 'texas':
                form_class = TexasNoTideEmailTemplateForm
            case 'ohio':
                form_class = OhioNoTideEmailtemplateForm
            case 'maac2-washington':
                form_class = MAAC2WashingtonNoTideTemplateForm
            case 'maac2-idaho':
                form_class = MAAC2IdahoNoTideTemplateForm
            case 'maac2-hawaii':
                form_class = MAAC2HawaiiNoTideTemplateForm
            case _:
                form_class = EmailTemplateForm

        form = form_class
        return render(request, 'no-tide-email-form-template.html', {'form': form})
    
    def post(self, request, name):
        selected_project = name

        match selected_project:
            case 'texas':
                form = TexasNoTideEmailTemplateForm(request.POST)
            case 'ohio':
                form = OhioNoTideEmailtemplateForm(request.POST)
            case 'maac2-washington':
                form = MAAC2WashingtonNoTideTemplateForm(request.POST)
            case 'maac2-idaho':
                form = MAAC2IdahoNoTideTemplateForm(request.POST)
            case 'maac2-hawaii':
                form = MAAC2HawaiiNoTideTemplateForm(request.POST)
            case _:
                form = EmailTemplateForm(request.POST)

        if form.is_valid():
            project = get_object_or_404(Project, name=selected_project)
            email_template = project.no_tide_email_template
            template_text = email_template.template_text
            formatted_text = template_text.format(**form.cleaned_data)
            return render(request, 'no-tide-email-form-template.html', {'form': form, 'formatted_text': formatted_text, 'selected_project': selected_project})
        
        return render(request, 'no-tide-email-form-template.html', {'form': form, 'selected_project': selected_project})

class ClearCacheAndCookiesView(View):
    def get(self, request):
        form = ClearCacheAndCookiesForm
        
        return render(request, 'no-tide-email-form-template.html', {'form': form, })
    
    def post(self, request):
        form = ClearCacheAndCookiesForm(request.POST)
        if form.is_valid():
            selected_project = form.cleaned_data['project']
            project = get_object_or_404(Project, name=selected_project)
            email_template = project.clear_cache_and_cookies_email_template
            template_text = email_template.template_text
            formatted_text = template_text.format(**form.cleaned_data)
            return render(request, 'no-tide-email-form-template.html', {'form': form, 'formatted_text': formatted_text, 'selected_project': selected_project})
        
        return render(request, 'no-tide-email-form-template.html', {'form': form, })