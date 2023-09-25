from django.db import models
from django.utils.text import slugify
import re

class Project(models.Model):
    name = models.CharField(max_length=40, default='Project Name')
    email_templates = models.ManyToManyField("CustomFormTemplate", related_name='projects_using_templates', blank=True)
    signature = models.TextField(max_length=400, default='Signature Goes Here', null=True)
    global_project = models.BooleanField(default=False)
    form_fields_created = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.signature = self.format_signature_for_html(self.signature)
        super(Project, self).save(*args, **kwargs)

        if not self.form_fields_created:
            form_fields_data = [
                {'label': 'Greeting', 'field_type': 'ChoiceField', 'required': True, 
                 'choices': 'Hello, Greetings, Good Morning, Good Afternoon, Good Evening'},
                {'label': 'Closing', 'field_type': 'ChoiceField', 'required': True, 
                 'choices': 'Thank You, Regards, Best Regards, Respectfully'},
                {'label': 'User Name', 'field_type': 'CharField', 'required': True},
                {'label': 'User Email', 'field_type': 'EmailField', 'required': True},
                {'label': 'User Phone', 'field_type': 'CharField', 'required': True},
                {'label': 'Agent Name', 'field_type': 'CharField', 'required': True},
                {'label': 'Coordinator Name', 'field_type': 'CharField', 'required': True},
                {'label': 'Coordinator Email', 'field_type': 'EmailField', 'required': True},
                {'label': 'Coordinator Phone', 'field_type': 'CharField', 'required': True},
                {'label': 'Correct EK', 'field_type': 'EKField', 'required': True},
                {'label': 'Incorrect EK', 'field_type': 'EKField', 'required': True},
                {'label': 'School Year', 'field_type': 'ChoiceField', 'required': True,
                 'choices': 'SY 21-22, SY 22-23, SY 23-24'},
                {'label': 'Results ID', 'field_type': 'IntegerField', 'required': True,},
                {'label': 'Case Number', 'field_type': 'IntegerField', 'required': True,},
                {'label': 'User Information Field', 'field_type': 'UserInfoField', 'required': True,},
            ]

            for field_data in form_fields_data:
                CustomFormField.objects.create(project=self, **field_data)

            self.form_fields_created = True
            self.save(update_fields=['form_fields_created'])

    def format_signature_for_html(self, signature):
        cleaned_signature = re.sub(r'\<br\>', '', signature)
        lines = cleaned_signature.split('\n')

        formatted_lines = []

        for line in lines:
            line = line.strip()
            formatted_lines.append(f'{line}<br>')

        html_formatted_signature = '\n'.join(formatted_lines)
        return html_formatted_signature
    
class CustomFormField(models.Model):
    FIELD_TYPES = [
        ('ChoiceField', 'ChoiceField'),
        ('IntegerField', 'IntegerField'),
        ('CharField', 'CharField'),
        ('EmailField', 'EmailField'),
        ('TextField', 'TextField'),
        ('EKField', 'EKField'),
        ('UserInfoField', 'UserInfoField')
    ]

    project = models.ForeignKey("Project", related_name='projects_using_fields', on_delete=models.CASCADE, blank=True, null=True)    
    label = models.CharField(max_length=40)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)
    choices = models.CharField(max_length=200, blank=True, null=True)
    template_code = models.CharField(max_length=61, default='', blank=True)
    template_format = models.CharField(max_length=62, default='', blank=True)
    
    def save(self, *args, **kwargs):
        self.template_code = '!' + self.label.lower()
        self.template_format = '{' + self.label.lower() + '}'
        super(CustomFormField, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.project.name} - {self.label}"

class CustomFormSignature(models.Model):
    project = models.ForeignKey(Project, related_name='signatures', on_delete=models.CASCADE, blank = True, null=True)
    signature_name = models.CharField(max_length=100, default='Signature')
    signature_text = models.TextField()

    def __str__(self):
        return f"{self.project.name.title()} - {self.signature_name}"

class CustomFormTemplate(models.Model):
    project = models.ForeignKey(Project, related_name='templates', on_delete=models.CASCADE, blank = True, null=True)
    template_name = models.CharField(max_length=100)
    template_slug = models.SlugField(unique=True, null=True, blank=True)
    fields = models.ManyToManyField(CustomFormField, blank=True)
    template_text = models.TextField()
    field_order_config = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.project.name.title()} - {self.template_name}"
    
    def save(self, *args, **kwargs):
        if not self.template_slug:
            self.template_slug = slugify(self.template_name)
        super().save(*args, **kwargs)
