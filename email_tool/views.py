from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import DeleteView
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .forms import (ProjectSelectionForm, TemplateBuilderForm, 
                    TemplateEditForm, AddProjectForm, EditSignatureForm,
                    FormCreatorForm, FormDeleteForm)
from .models import Project, CustomFormTemplate, CustomFormField, CustomFormSignature
from django import forms
from django.core.exceptions import ValidationError
import re
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.contrib import messages

class ProjectSelectionView(View):
    def get(self, request):
        form = ProjectSelectionForm()
        selected_project = None
        return render(request, 'home.html', {'form': form, 'selected_project': selected_project,})
    
    def post(self, request):
        form = ProjectSelectionForm(request.POST)
        if form.is_valid():
            selected_project = form.cleaned_data['project']
            project = Project.objects.get(pk=selected_project)
            return HttpResponseRedirect(reverse('project-landing-page', args=[project.name]))
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
    
class AdminPanelView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProjectSelectionForm()
        selected_project = None
        return render(request, 'admin-panel.html', {'form': form, 'selected_project': selected_project})
    
    def post(self, request):
        form = ProjectSelectionForm(request.POST)
        if form.is_valid():
            selected_project = form.cleaned_data['project']
            project = Project.objects.get(pk=selected_project)
            link = request.POST.get('button_name')
            return HttpResponseRedirect(reverse(link, args=[project.name]))
        else:
            return render(request, 'admin-panel.html', {'form': form}) 
        
class ViewEditTemplateView(LoginRequiredMixin, View):
    def get(self, request, name):
        selected_project_name = name
        selected_project = get_object_or_404(Project, name=name)
        email_templates = selected_project.email_templates.all()
        return render(request, 'view-edit-templates.html', {'selected_project_name': selected_project_name, 'selected_project': selected_project,'email_templates': email_templates})
    
    def post(self, request, name):
        selected_project_name = name
        template_name = request.POST.get('template_name', None)
        current_template = get_object_or_404(CustomFormTemplate, template_name=template_name)
        template_slug = current_template.template_slug
        return HttpResponseRedirect(reverse('edit-template', args=[name, template_slug]))
    
class EditTemplateView(LoginRequiredMixin, View):
    def get(self, request, name, template_slug):
        selected_project_name = name
        selected_project = get_object_or_404(Project, name=name)
        selected_template = get_object_or_404(CustomFormTemplate, template_slug=template_slug)
        initial_fields = CustomFormField.objects.filter(project=selected_project)
        selected_agent_fields = {field.template_format: field.template_code.title() for field in initial_fields}
        template_with_reverse_formatted_fields = self.reverse_text_replace(selected_agent_fields, selected_template.template_text)
        html_formatted_email_safe  = mark_safe(selected_template.template_text)
        template_with_no_html_tags = self.remove_tags(template_with_reverse_formatted_fields)
        
        form = TemplateEditForm(project=selected_project, initial={ 
            'template_name': selected_template.template_name,
            'template': template_with_no_html_tags,
            'formatted_template': html_formatted_email_safe,
            'agent_fields': selected_template.fields.all(),
        })

        return render(request, "edit-template.html", {
            'form': form, 
            'selected_template': selected_template,
            'selected_project_name': selected_project_name, 
            'selected_project': selected_project, 
            'preview_template': html_formatted_email_safe,
            'template_slug': template_slug,
            }
        )
    
    def post(self, request, name, template_slug):
        selected_project_name = name
        selected_project = get_object_or_404(Project, name=selected_project_name)
        form = TemplateBuilderForm(request.POST, project=selected_project)
        if 'format' in request.POST:
            if form.is_valid():
                selected_project_name = name
                selected_project = get_object_or_404(Project, name=selected_project_name)
                template_name = form.cleaned_data['template_name']
                selected_template = form.cleaned_data['template']
                selected_agent_fields = form.cleaned_data['agent_fields']
                template_with_formatted_fields = self.text_replace(selected_agent_fields, selected_template)
                html_formatted_email = self.format_template_for_html(template_with_formatted_fields) 
                html_formatted_email_safe  = mark_safe(html_formatted_email)
                
                form = TemplateEditForm(project=selected_project, initial={
                    'template_name': template_name,
                    'template': selected_template,
                    'formatted_template': html_formatted_email,
                    'agent_fields': selected_agent_fields,
                })

                return render(request, "edit-template.html", {
                    'form': form, 
                    'selected_template': selected_template,
                    'selected_project_name': selected_project_name, 
                    'selected_project': selected_project, 
                    'preview_template': html_formatted_email_safe,
                    'template_slug': template_slug,
                    })
            else:
                return render(request, "edit-template.html", {'form': form})
            
        elif 'save' in request.POST:
            if form.is_valid():
                selected_project_name = name
                selected_project = get_object_or_404(Project, name=name)
                template_name = form.cleaned_data['template_name']
                selected_template = form.cleaned_data['template']
                selected_agent_fields = form.cleaned_data['agent_fields']
                template_with_formatted_fields = self.text_replace(selected_agent_fields, selected_template)
                html_formatted_email = self.format_template_for_html(template_with_formatted_fields) 
                field_order_config = self.get_field_order_config(template_with_formatted_fields)

                custom_template, created = CustomFormTemplate.objects.get_or_create(
                    project = selected_project,
                    template_name = template_name,
                    template_slug = template_slug
                )
                custom_template.template_text = html_formatted_email 
                custom_template.fields.set(selected_agent_fields)
                custom_template.field_order_config = field_order_config
                custom_template.save()
                selected_project.email_templates.add(custom_template)

                return HttpResponseRedirect(reverse('view-edit-templates', args=[selected_project.name]))
            
        else:
            selected_template = get_object_or_404(CustomFormTemplate, project=selected_project, template_slug=template_slug)
            selected_template.delete()

            return HttpResponseRedirect(reverse('template_delete_confirmation_view'))
            
    def reverse_text_replace(self, selected_agent_fields, selected_template):
        replacements = selected_agent_fields

        signature = '{Signature}'
        replacements[signature] = '!Signature'
        
        for old_word, new_word in replacements.items():
            selected_template = re.sub(re.escape(old_word), new_word, selected_template, flags=re.IGNORECASE)

        return selected_template
    
    def remove_tags(self, form_data):
        remove_front_span = re.sub(r'<span[^>]*>', '', form_data)
        remove_back_span = re.sub(r'</span>', '', remove_front_span)
        remove_front_p = re.sub(r'<p[^>]*>','', remove_back_span)
        remove_back_p = re.sub(r'</p>', '', remove_front_p)
        remove_breaks = re.sub(r'<br>', ' !P', remove_back_p)
        form_data = remove_breaks
        return form_data
    
    def format_template_for_html(self, template_with_formatted_fields):
        lines = template_with_formatted_fields.split('\n')

        formatted_lines = []

        for line in lines:
            line = line.strip()
            if line.strip().endswith('!P'):
                line_no_p = line.strip("!P").strip()
                formatted_lines.append(f'{line_no_p}<br>')
            else:
                formatted_lines.append(f'<p>{line}</p>')

        html_formatted_email = '\n'.join(formatted_lines)
        return html_formatted_email

    def get_field_order_config(self, formatted_template):
        reg_format = re.compile(r'\{([^}]+)\}')
        match = reg_format.findall(formatted_template)
        field_order_config = {}
        for index, m in enumerate(match):
            field_order_config[m] = index
        
        return field_order_config

    def text_replace(self, selected_agent_fields, template):
        replacements = {}
        for field in selected_agent_fields:
            replacements[field.template_code.title()] = f'<span class="template-text-color">{field.template_format.title()}</span>'

        signature = "{Signature}"
        replacements['!Signature'] = f'<span class="template-text-color">{signature}</span>'
        
        for old_word, new_word in replacements.items():
            template = re.sub(re.escape(old_word), new_word, template, flags=re.IGNORECASE)

        return template

class CreateEmailView(View):
    def get(self, request, name, template_name):
        selected_project_name = name
        selected_project = get_object_or_404(Project, name=name)
        try:
            template = get_object_or_404(CustomFormTemplate, project=selected_project, template_name=template_name)
        except CustomFormTemplate.DoesNotExist:
            template = None

        form_fields = self.get_field_order(template)

        CustomEmailForm = type('CustomEmailForm', (forms.Form,), form_fields)
        form = CustomEmailForm
        return render(request, 'email-template.html', {'form': form, 'selected_project': selected_project, 'selected_project_name': selected_project_name})
    
    def post(self, request, name, template_name):
        selected_project_name = name.upper()
        selected_project = get_object_or_404(Project, name=name)
        try:
            template = get_object_or_404(CustomFormTemplate, project=selected_project, template_name=template_name)
        except CustomFormTemplate.DoesNotExist:
            template = None

        form_fields = self.get_field_order(template)
        
        CustomEmailForm = type('CustomEmailForm', (forms.Form,), form_fields)
        form = CustomEmailForm(request.POST)
             
        if form.is_valid():
            template_text = template.template_text
            template_text = self.remove_span_tags(template_text)
            form_data = form.cleaned_data.copy()
            if 'User Information Field' in form_data:
                form_data['User Information Field'] = self.format_customer_information(form_data)
            if 'Results ID' in form_data:
                form_data['Results ID'] = self.format_results_ids(form_data)

            form_data['Signature'] = selected_project.signature

            formatted_text = template_text.format(**form_data)

            return render(request, 'email-template.html', {'form': form, 'formatted_text':  formatted_text, 'selected_project': selected_project, 'selected_project_name': selected_project_name})
        else:
            return render(request, 'email-template.html', {'form': form})
        
    def remove_span_tags(self, form_data):
        remove_front_span = re.sub(r'<span[^>]*>', '', form_data)
        remove_back_span = re.sub(r'</span>', '', remove_front_span)
        form_data = remove_back_span
        return form_data
    
    def get_field_order(self, template):
        form_fields = {}
        field_order_config = template.field_order_config
        sorted_fields = sorted(template.fields.all(), key=lambda field: field_order_config.get(field.label, 0))
        for field in sorted_fields:
            field_type = field.field_type
            field_choices = field.choices.split(',') if field.choices else []
            field_required = field.required

            if field_type == 'CharField':
                form_fields[field.label] = forms.CharField(
                    required=field_required,
                    label = field.label,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                )
            elif field_type == 'EmailField':
                form_fields[field.label] = forms.EmailField(
                    required=field_required,
                    label = field.label,
                    widget=forms.EmailInput(attrs={'class': 'form-control'}),
                )
            elif field_type == 'ChoiceField':
                form_fields[field.label] = forms.ChoiceField(
                    choices=[(choice.strip(), choice.strip()) for choice in field_choices],
                    required=field_required,
                    label = field.label,
                    widget=forms.Select(attrs={'class': 'form-control'}),
                )
            elif field_type == 'IntegerField':
                form_fields[field.label] = forms.IntegerField(
                    required=field_required,
                    label = field.label,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                )
            elif field_type == 'EKField':
                form_fields[field.label] = forms.IntegerField(
                    required=field_required,
                    label = field.label,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    validators=[self.validate_ekfield]
                )
            elif field_type == 'TextField':
                form_fields[field.label] = forms.CharField(
                    required=field_required,
                    label = field.label,
                    widget=forms.Textarea(attrs={'class': 'form-control'}),
                )
            elif field_type == 'UserInfoField':
                form_fields[field.label] = forms.CharField(
                    required=field_required,
                    label = field.label,
                    widget=forms.Textarea(attrs={'class': 'form-control'}),
                )
        return form_fields

    def validate_ekfield(self, value):
        if value is not None and (value < 0 or value > 99999999):
            raise ValidationError('Must be a valid EK Number. Make sure you are not providing a Student Id!')
    
    def format_customer_information(self, form_data):
        remove_all_before_name = re.sub(r'.*Close', 'Name:', form_data['User Information Field'], flags=re.DOTALL)
        remove_create_date_and_beyond = re.sub(r'Create Date:.+', 'Case Creation Date:', remove_all_before_name, flags=re.DOTALL)
        remove_customer_id = re.sub(r'\[(.*?)Voice:', 'Voice:', remove_create_date_and_beyond, flags=re.DOTALL)
        remove_alternative = re.sub(r'Alternative:(.*?)Project State:', 'Project State:', remove_customer_id, flags=re.DOTALL)
        remove_region_code = re.sub(r'Region Code:(.*?)Region:', 'Region:', remove_alternative, flags=re.DOTALL)
        remove_fax = re.sub(r'\bFax:\s*', '', remove_region_code)
        clean_results = remove_fax

        customer_info_lines = clean_results.split('\n')
        filtered_lines = [line for line in customer_info_lines if line.strip()]
        words_to_check = ["Name", "Voice", "Email", "Company", "Project State", "Region", "District Code", "District", "School Code", "Case Creation Date:"]
        formatted_customer_info = []
        skip_next = False
        for i in range(len(filtered_lines)):
            if skip_next:
                skip_next = False
                continue

            line = filtered_lines[i].strip()
            if i + 1 < len(filtered_lines) and not any(filtered_lines[i + 1].strip().startswith(word + ':') for word in words_to_check):
                formatted_customer_info.append(f'{line} {filtered_lines[i + 1].strip()} {"<br>"}')
                skip_next = True
            else:
                formatted_customer_info.append(f'{line}{"<br>"}')

        block_of_customer_info = '\n'.join(formatted_customer_info)
        return block_of_customer_info
        
    def format_results_ids(self, form_data):
        formatted_results = 'RID: ' + ', RID: '.join([value.strip() for value in re.split(r'[ ,]+', form_data['Results ID'])])
        return formatted_results

class TemplateBuildView(LoginRequiredMixin, View):
    def get(self, request, name):
        selected_project_name = name.title()
        selected_project = get_object_or_404(Project, name=name)
        initial_fields = CustomFormField.objects.filter(project=selected_project)

        form = TemplateBuilderForm(project = selected_project)
        return render(request, "template-builder.html", {
            'form': form, 
            'selected_project_name': selected_project_name, 
            'selected_project': selected_project, 
            })
    
    def post(self, request, name):
        selected_project = get_object_or_404(Project, name=name)
        form = TemplateBuilderForm(request.POST, project = selected_project)
        if 'format' in request.POST:
            if form.is_valid():
                template_name = form.cleaned_data['template_name']
                saved_template_text = form.cleaned_data['template']
                selected_agent_fields = form.cleaned_data['agent_fields']
                template_with_formatted_fields = self.text_replace(selected_agent_fields, saved_template_text)
                html_formatted_email = self.format_template_for_html(template_with_formatted_fields) 
                html_formatted_email_safe  = mark_safe(html_formatted_email)
                form.cleaned_data['formatted_template'] = html_formatted_email
                
                form = TemplateBuilderForm(project = selected_project,
                    initial={
                        'formatted_template': html_formatted_email,
                        'template': saved_template_text,
                        'template_name': template_name,
                        'project_selection': selected_project,
                        'agent_fields': selected_agent_fields,
                    }
                ) 
                
                return render(request, "template-builder.html", {
                    'form': form, 
                    'selected_project': selected_project, 
                    'preview_text': html_formatted_email_safe,
                    })
            else:
                print('invalid')
                return render(request, "template-builder.html", {'form': form, 'selected_project':selected_project})
            
        elif 'save' in request.POST:
            if form.is_valid():
                selected_project = get_object_or_404(Project, name=name)
                template_name = form.cleaned_data['template_name']
                formatted_template = request.POST.get('formatted_template', '')
                selected_field_ids = form.cleaned_data['agent_fields']
                field_order_config = self.get_field_order_config(formatted_template)

                custom_template, created = CustomFormTemplate.objects.get_or_create(
                    project = selected_project,
                    template_name = template_name,
                )
                custom_template.template_text = formatted_template 
                custom_template.fields.set(selected_field_ids)
                custom_template.field_order_config = field_order_config
                custom_template.save()
                selected_project.email_templates.add(custom_template)

                return HttpResponseRedirect(reverse('view-edit-templates', args=[selected_project.name]))
        
    def format_template_for_html(self, template_with_formatted_fields):
        lines = template_with_formatted_fields.split('\n')

        formatted_lines = []

        for line in lines:
            line = line.strip()
            if line.strip().endswith('!P'):
                line_no_p = line.strip("!P").strip()
                formatted_lines.append(f'{line_no_p}<br>')
            else:
                formatted_lines.append(f'<p>{line}</p>')

        html_formatted_email = '\n'.join(formatted_lines)
        return html_formatted_email

    def get_field_order_config(self, formatted_template):
        reg_format = re.compile(r'\{([^}]+)\}')
        match = reg_format.findall(formatted_template)
        field_order_config = {}
        for index, m in enumerate(match):
            field_order_config[m] = index
        
        return field_order_config

    def text_replace(self, selected_agent_fields, template):
        replacements = {}
        for field in selected_agent_fields:
            replacements[field.template_code.title()] = f'<span class="template-text-color">{field.template_format.title()}</span>'

        signature = "{Signature}"
        replacements['!Signature'] = f'<span class="template-text-color">{signature}</span>'
        
        for old_word, new_word in replacements.items():
            template = re.sub(re.escape(old_word), new_word, template, flags=re.IGNORECASE)

        return template
    
class ProjectAddView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddProjectForm()
        return render(request, 'add-project.html', {'form': form})
    
    def post(self, request):
        form = AddProjectForm(request.POST)
        if form.is_valid():
            project_name = form.cleaned_data['name']
            project_signature = form.cleaned_data['signature']

            try:
                project = Project.objects.get(name=project_name.title())
                messages.error(request, 'Project already exists!')
                return render(request, 'add-project.html', {'form': form})   
            except Project.DoesNotExist:       
                new_project, created = Project.objects.get_or_create(
                    name=project_name.title(),
                    signature=project_signature
                )
                new_project.save()
                return HttpResponseRedirect(reverse('admin-panel'))    
            
class EditSignatureView(LoginRequiredMixin, View):
    def get(self, request, name):
        selected_project = get_object_or_404(Project, name=name)
        signature = self.remove_tags(selected_project.signature)
        form = EditSignatureForm(initial={
            'signature': signature
            }
        )
        return render(request, 'edit-signature.html', {'form': form, 'selected_project': selected_project})
    
    def post(self, request, name):
        form = EditSignatureForm(request.POST)
        if form.is_valid():
            selected_project = get_object_or_404(Project, name=name)
            project_signature = form.cleaned_data['signature']

            selected_project.signature = project_signature
            selected_project.save()
            return HttpResponseRedirect(reverse('admin-panel'))

            
    def remove_tags(self, signature):
        remove_breaks = re.sub(r'<br>', '', signature)
        signature = remove_breaks
        return signature
    
class FormCreatorView(LoginRequiredMixin, View):
    def get(self, request, name):
        selected_project_name = name.title()
        selected_project = get_object_or_404(Project, name=selected_project_name)
        form = FormCreatorForm()
        return render(request, 'form-creator.html', {'form': form, 'selected_project': selected_project})
    
    def post(self, request, name):
        form = FormCreatorForm(request.POST)
        if form.is_valid():
            selected_project_name = name.title()
            selected_project = get_object_or_404(Project, name=selected_project_name)
            label = form.cleaned_data['label'].title()
            field_type = form.cleaned_data['field_type']
            required = form.cleaned_data['required']
            choices = form.cleaned_data['choices']
            try:
                form_field = CustomFormField.objects.get(label=label, project=selected_project)
                messages.error(request, 'Form with that name already exists!')
                return render(request, 'form-creator.html', {'form': form, 'selected_project': selected_project})   
            except CustomFormField.DoesNotExist:       
                new_form_field, created = CustomFormField.objects.get_or_create(
                    project=selected_project,
                    label = label,
                    field_type = field_type,
                    required = required,
                    choices = choices
                )
                new_form_field.save()
                return HttpResponseRedirect(reverse('admin-panel'))    
            
class FormDeleteView(LoginRequiredMixin, View):
    def get(self, request, name):
        selected_project_name = name.title()
        selected_project = get_object_or_404(Project, name=selected_project_name)
        form = FormDeleteForm(project=selected_project)
        return render(request, 'form-delete.html', {'form': form, 'selected_project': selected_project})
    
    def post(self, request, name):
        selected_project_name = name.title()
        selected_project = get_object_or_404(Project, name=selected_project_name)
        form = FormDeleteForm(request.POST, project=selected_project)

        if form.is_valid():
            selected_forms_fields = form.cleaned_data['form_fields']

            for field in selected_forms_fields:
                CustomFormField.objects.filter(project=selected_project, label=field.label).delete()

            return HttpResponseRedirect(reverse('form_delete_confirmation_view'))
        
def template_delete_confirmation_view(request):
    return render(request, 'template-delete-confirmation.html')

def form_delete_confirmation_view(request):
    return render(request, 'form-delete-confirmation.html')

def about_view(request):
    return render(request, 'about.html')
