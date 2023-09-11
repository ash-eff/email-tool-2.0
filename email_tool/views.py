from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import NoTideAccountForm, EmailTemplateForm, TexasEmailTemplateForm, OhioEmailtemplateForm, MAAC2WashingtonTemplateForm, MAAC2IdahoTemplateForm, MAAC2HawaiiTemplateForm
from .models import EmailTemplate, Project

def home_page(request):
    return render(request, 'home.html')

class NoTideAccountView(View):
    def get(self, request):
        form = NoTideAccountForm()
        return render(request, 'no-tide-account.html', {'form': form})
    
    def post(self, request):
        form = NoTideAccountForm(request.POST)
        if form.is_valid():
            selected_project = form.cleaned_data['project']
            return HttpResponseRedirect(reverse('email-form-template', args=[selected_project]))  
          
class EmailTemplateView(View):
    def get(self, request, name):
        selected_project = name

        match selected_project:
            case 'texas':
                form_class = TexasEmailTemplateForm
            case 'ohio':
                form_class = OhioEmailtemplateForm
            case 'maac2-washington':
                form_class = MAAC2WashingtonTemplateForm
            case 'maac2-idaho':
                form_class = MAAC2IdahoTemplateForm
            case 'maac2-hawaii':
                form_class = MAAC2HawaiiTemplateForm
            case _:
                form_class = EmailTemplateForm

        form = form_class
        return render(request, 'email-form-template.html', {'form': form})
    
    def post(self, request, name):
        selected_project = name

        match selected_project:
            case 'texas':
                form = TexasEmailTemplateForm(request.POST)
            case 'ohio':
                form = OhioEmailtemplateForm(request.POST)
            case 'maac2-washington':
                form = MAAC2WashingtonTemplateForm(request.POST)
            case 'maac2-idaho':
                form = MAAC2IdahoTemplateForm(request.POST)
            case 'maac2-hawaii':
                form = MAAC2HawaiiTemplateForm(request.POST)
            case _:
                form = EmailTemplateForm(request.POST)

        if form.is_valid():
            project = get_object_or_404(Project, name=selected_project)
            email_template = project.email_template
            template_text = email_template.template_text
            formatted_text = template_text.format(**form.cleaned_data)
            return render(request, 'email-form-template.html', {'form': form, 'formatted_text': formatted_text, 'selected_project': selected_project})
        
        return render(request, 'email-form-template.html', {'form': form, 'selected_project': selected_project})

