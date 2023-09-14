from django.db import models

class Project(models.Model):
    PROJECTS = [
        ('indiana', 'Indiana'),
        ('maac2-hawaii', 'MAAC2 - Hawaii'), 
        ('maac2-idaho', 'MAAC2 - Idaho'), 
        ('maac2-washington', 'MAAC2 - Washington'), 
        ('ohio', 'Ohio'),
        ('texas', 'Texas'),
    ]
    name = models.CharField(max_length=30)
    project = models.CharField(max_length=30)
    email_templates = models.ManyToManyField("EmailTemplate")

    def __str__(self):
        return self.name

class EmailTemplate(models.Model):
    subject = models.CharField(max_length=100)
    custom_form_template = models.ForeignKey("CustomFormTemplate", on_delete=models.CASCADE)
    template_text = models.TextField()

    def __str__(self):
        return self.subject
    
class CustomFormField(models.Model):
    LABEL_CHOICES = [
        ('Greeting', 'Greeting'),
        ('Closing', 'Closing'),
        ('User Name', 'User Name'),
        ('User Email', 'User Email'),
        ('Case Number', 'Case Number'), 
        ('Agent Name', 'Agent Name'),
        ('Coordinator Choices', 'Coordinator Choices'),
        ('Coordinator Name', 'Coordinator Name'),
        ('Coordinator Email', 'Coordinator Email'),
        ('Coordinator Phone', 'Coordinator Phone'),
    ]

    FIELD_TYPES = [
        ('ChoiceField', 'ChoiceField'),
        ('IntegerField', 'IntegerField'),
        ('CharField', 'CharField'),
        ('EmailField', 'EmailField'),
    ]

    TITLE_CHOICES = [
        ('All Projects', 'All Projects'),
        ('Indiana', 'Indiana'),
        ('MAAC2-hawaii', 'MAAC2 - Hawaii'), 
        ('MAAC2-idaho', 'MAAC2 - Idaho'), 
        ('MAAC2-washington', 'MAAC2 - Washington'), 
        ('Ohio', 'Ohio'),
        ('Texas', 'Texas'),
    ]

    title = models.CharField(max_length=100, choices=TITLE_CHOICES)
    label = models.CharField(max_length=20, choices=LABEL_CHOICES)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)
    choices = models.CharField(max_length=200, blank=True, null=True) 

    def __str__(self):
        return f"{self.title} - {self.get_label_display()}"
    
class CustomFormTemplate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    template_name = models.CharField(max_length=100)
    fields = models.ManyToManyField(CustomFormField, blank=True)

    def __str__(self):
        return self.template_name
