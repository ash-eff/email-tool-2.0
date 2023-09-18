from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import (ProjectSelectionForm, TemplateBuilderForm)
from .models import Project, CustomFormTemplate, CustomFormField
from django import forms
from django.core.exceptions import ValidationError
import re
from django.utils.safestring import mark_safe
from django.db.models import Q

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
            template = None

        field_order_config = template.field_order_config
        form_fields = {}
        sorted_fields = sorted(template.fields.all(), key=lambda field: field_order_config.get(f"{field.label} {field.label_two}" if field.label_two else field.label, 0))
        for field in sorted_fields:
            con_field_name = field.label + ' ' + field.label_two if field.label_two is not None else field.label
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
            template = None

        field_order_config = template.field_order_config
        form_fields = {}
        sorted_fields = sorted(template.fields.all(), key=lambda field: field_order_config.get(f"{field.label} {field.label_two}" if field.label_two else field.label, 0))
        for field in sorted_fields:
            con_field_name = field.label + ' ' + field.label_two if field.label_two is not None else field.label
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
            greeting = '<p>{Greeting} {User Name},</p>'
            template_text = greeting + template.template_text + selected_project.signature.signature_text
            form_data = form.cleaned_data.copy()
            form_data['Results ID'] = self.format_results_ids
            formatted_text = template_text.format(**form_data)

            return render(request, 'email-template.html', {'form': form, 'formatted_text':  formatted_text, 'selected_project': selected_project, 'selected_project_name': selected_project_name})
        else:
            return render(request, 'email-template.html', {'form': form})
        
    def validate_ekfield(self, value):
        if value is not None and (value < 0 or value > 99999999):
            raise ValidationError('Must be a valid EK Number. Make sure you are not providing a Student Id!')
        
    def format_results_ids(self):
        result_id = self.form.data.get('Results ID', '')
        formatted_results = 'RID: ' + ', RID: '.join([value.strip() for value in re.split(r'[ ,]+', result_id)])
        return formatted_results

class TemplateBuildView(View):
    def get(self, request, name):
        selected_project = get_object_or_404(Project, name=name)
        initial_fields = CustomFormField.objects.filter(Q(title='Texas') | Q(title='All Projects'))
        form = TemplateBuilderForm(initial={'fields': initial_fields.values_list('id', flat=True)})
        return render(request, "template-builder.html", {'form': form, 'selected_project': selected_project})
    
    def post(self, request, name):
        form = TemplateBuilderForm(request.POST,)
        
        if 'format' in request.POST:
            if form.is_valid():
                selected_project = get_object_or_404(Project, name=name)
                template_name = form.cleaned_data['template_name']
                saved_template = form.cleaned_data['template']
                selected_fields = form.cleaned_data['fields'] 
                replaced_text = self.text_replace(saved_template)
                formatted_email = self.format_template(replaced_text) 
                formatted_email_safe  = mark_safe(formatted_email)
                form.cleaned_data['formatted_template'] = formatted_email
                
                form = TemplateBuilderForm(
                    initial={
                        'formatted_template': formatted_email,
                        'template': saved_template,
                        'template_name': template_name,
                        'project_selection': selected_project,
                        'fields': selected_fields.values_list('id', flat=True),
                    }
                ) 
                
                return render(request, "template-builder.html", {'form': form, 'selected_project': selected_project, 'preview_text': formatted_email_safe})
            else:
                return render(request, "template-builder.html", {'form': form})
            
        elif 'save' in request.POST:
            if form.is_valid():
                selected_project = get_object_or_404(Project, name=name)
                template_name = form.cleaned_data['template_name']
                formatted_template = request.POST.get('formatted_template', '')
                selected_field_ids = form.cleaned_data['fields']

                custom_template, created = CustomFormTemplate.objects.get_or_create(
                    project_name = selected_project.project,
                    template_name = template_name,
                )
                custom_template.template_text = formatted_template 
                custom_template.fields.set(selected_field_ids)
                custom_template.save()

                return HttpResponseRedirect(reverse('project-landing-page', args=[selected_project.name]))
        
    def format_template(self, replaced_text):
        lines = replaced_text.split('\n')

        formatted_lines = []

        for line in lines:
            line = line.strip()
            if line.strip().endswith('!P'):
                line_no_p = line.strip("!P").strip()
                formatted_lines.append(f'{line_no_p}<br>')
            else:
                formatted_lines.append(f'<p>{line}</p>')

        formatted_email = '\n'.join(formatted_lines)
        return formatted_email

    

    # these need to be their own model, or at least part of the project model
    def get_signature(self, selected_project):
        signature = ''
        if selected_project == 'texas':
            signature = """
                <p>{Closing},<br>
                {Agent Name}</span><br>
                Texas Testing Support<br>
                Phone: 833-601-8821<br>
                Email: TexasTestingSupport@cambiumassessment.com<br>
                https://TexasAssessment.gov</p>
            """
        elif selected_project == 'ohio':
            signature = """
                <p><span class="template-text-color">{Closing},<br>
                {Agent Name}</span><br>
                Ohio Help Desk<br>
                Tel 1.877.231.7809<br>
                Fax 1.877.218.7663<br>
                ohhelpdesk@cambiumassessment.com<br>
            """
        elif selected_project == 'indiana':
            signature = """
                <p><span class="template-text-color">{Closing},<br>
                {Agent Name}</span><br>
                Indiana Assessment Help Desk<br>
                Cambium Assessment, Inc.<br>
                Tel 1.866.298.4256<br>
                Email indianahelpdesk@cambiumassessment.com</p>
            """
        elif selected_project == 'washington':
            signature = """
                <p><span class="template-text-color">{Closing},<br>
                {Agent Name}</span><br>
                Washington Help Desk<br>
                Cambium Assessment, Inc.<br>
                Tel 1.844.560.7366<br>
                wahelpdesk@cambiumassessment.com</p><br>
            """
        elif selected_project == 'hawaii':
            signature = """
                <p><span class="template-text-color">{Closing},<br>
                {Agent Name}</span><br>
                HSAP Help Desk<br>
                Cambium Assessment, Inc.<br>
                Tel 1.866.648.3712<br>
                Fax 1.877.218.7663<br>
                hsaphelpdesk@cambiumassessment.com</p><br>
            """
        elif selected_project == 'idaho':
            signature = """
                <p><span class="template-text-color">{Closing},<br>
                {Agent Name}</span><br>
                Idaho Help Desk<br>
                Cambium Assessment, Inc.<br>
                Tel 1.844.560.7365<br>
                Fax 1.877.218.7663<br>
                idhelpdesk@cambiumassessment.com</p><br>
            """
        return signature
        

    #create a dict from models and map here to iterate 
    def text_replace(self, template):
        replacements = {
            "!greeting": '<span class="template-text-color">{Greeting}</span>',
            "!user name": '<span class="template-text-color">{User Name}</span>',
            "!coordinator choices": '<span class="template-text-color">{Coordinator Choices}</span>',
            "!coordinator name": '<span class="template-text-color">{Coordinator Name}</span>',
            "!coordinator email": '<span class="template-text-color">{Coordinator Email}</span>',
            "!coordinator phone": '<span class="template-text-color">{Coordinator Phone}</span>',
            "!case number": '<span class="template-text-color">{Case Number}</span>',
            "!closing": '<span class="template-text-color">{Closing}</span>',
            "!agent name": '<span class="template-text-color">{Agent Name}</span>',
            "!signature": '<span class="template-text-color">{Signature}</span>',
        }

        for old_word, new_word in replacements.items():
            template = re.sub(re.escape(old_word), new_word, template, flags=re.IGNORECASE)

        return template