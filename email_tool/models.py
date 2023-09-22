from django.db import models
from django.utils.text import slugify

class Project(models.Model):
    name = models.CharField(max_length=40, default='Project Name')
    email_templates = models.ManyToManyField("CustomFormTemplate", related_name='projects_using_templates', blank=True)
    signature = models.TextField(max_length=400, default='Signature Goes Here', null=True)
    global_project = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.signature = self.format_signature_for_html(self.signature)
        super().save(*args, **kwargs)

    def format_signature_for_html(self, signature):
        lines = signature.split('\n')

        formatted_lines = []

        for line in lines:
            line = line.strip()
            formatted_lines.append(f'{line}<br>')

        html_formatted_signature = '\n'.join(formatted_lines)
        return html_formatted_signature
    
class CustomFormField(models.Model):
    LABEL_CHOICES = [
        ('Greeting', 'Greeting'),
        ('Closing', 'Closing'),
        ('User Name', 'User Name'),
        ('User Email', 'User Email'),
        ('Case Number', 'Case Number'), 
        ('Agent Name', 'Agent Name'),
        ('Coordinator Choices', 'Coordinator Choices'),
        ('Coordinator Choices Abbreviated', 'Coordinator Choices Abbreviated'),
        ('Coordinator Name', 'Coordinator Name'),
        ('Coordinator Email', 'Coordinator Email'),
        ('Coordinator Phone', 'Coordinator Phone'),
        ('Incorrect EK', 'Incorrect EK'),
        ('Correct EK', 'Correct EK'),
        ('School Year', 'School Year'),
        ('Results ID', 'Results ID'),
        ('General Choice Field', 'General Choice Field'),
        ('General Integer Field', 'General Integer Field'),
        ('General Text Field', 'General Text Field'),
    ]

    FIELD_TYPES = [
        ('ChoiceField', 'ChoiceField'),
        ('IntegerField', 'IntegerField'),
        ('CharField', 'CharField'),
        ('EmailField', 'EmailField'),
        ('TextField', 'TextField'),
        ('EKField', 'EKField'),
    ]

    project = models.ForeignKey("Project", related_name='projects_using_fields', on_delete=models.CASCADE, blank=True, null=True)    
    label = models.CharField(max_length=60, choices=LABEL_CHOICES)
    label_two = models.CharField(max_length=30, blank=True, null=True)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)
    choices = models.CharField(max_length=200, blank=True, null=True)
    template_code = models.CharField(max_length=61, default='', blank=True)
    template_format = models.CharField(max_length=62, default='', blank=True)

    def is_global_field(self):
        return self.projects is None or self.projects.filter(global_project=True).exists()
    
    def save(self, *args, **kwargs):
        self.template_code = '!' + self.label.lower()
        self.template_format = '{' + self.label.lower() + '}'
        super(CustomFormField, self).save(*args, **kwargs)

    def __str__(self):
        label_two_display = ''
        if self.label_two != None:
            label_two_display = self.label_two

        return self.get_label_display()
        #return f"{self.title} - {self.get_label_display()} {label_two_display}"

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
