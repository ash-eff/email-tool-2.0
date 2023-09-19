from django.db import models

PROJECTS = [
        ('indiana', 'Indiana'),
        ('hawaii', 'Hawaii'), 
        ('idaho', 'Idaho'), 
        ('washington', 'Washington'), 
        ('ohio', 'Ohio'),
        ('texas', 'Texas'),
    ]

class Project(models.Model):
    name = models.CharField(max_length=30)
    project = models.CharField(max_length=100, choices=PROJECTS)
    email_templates = models.ManyToManyField("CustomFormTemplate", blank=True)
    signature = models.ForeignKey('CustomFormSignature', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
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
        ('Signature', 'Signature'),
        ('Internal Teams', 'Internal Teams'),
    ]

    FIELD_TYPES = [
        ('ChoiceField', 'ChoiceField'),
        ('IntegerField', 'IntegerField'),
        ('CharField', 'CharField'),
        ('EmailField', 'EmailField'),
        ('TextField', 'TextField'),
        ('EKField', 'EKField'),
    ]

    TITLE_CHOICES = [
        ('All Projects', 'All Projects'),
        ('Indiana', 'Indiana'),
        ('hawaii', 'Hawaii'), 
        ('idaho', 'Idaho'), 
        ('washington', 'Washington'), 
        ('Ohio', 'Ohio'),
        ('Texas', 'Texas'),
    ]

    title = models.CharField(max_length=100, choices=TITLE_CHOICES)
    label = models.CharField(max_length=60, choices=LABEL_CHOICES)
    label_two = models.CharField(max_length=30, blank=True, null=True)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)
    choices = models.CharField(max_length=200, blank=True, null=True) 

    def __str__(self):
        label_two_display = ''
        if self.label_two != None:
            label_two_display = self.label_two
        return self.get_label_display()
        #return f"{self.title} - {self.get_label_display()} {label_two_display}"

class CustomFormSignature(models.Model):
    project_name = models.CharField(max_length=100, choices=PROJECTS)
    signature_name = models.CharField(max_length=100, default='Signature')
    signature_text = models.TextField()

    def __str__(self):
        return f"{self.project_name.title()} - {self.signature_name}"

class CustomFormTemplate(models.Model):
    project_name = models.CharField(max_length=100, choices=PROJECTS)
    template_name = models.CharField(max_length=100)
    fields = models.ManyToManyField(CustomFormField, blank=True)
    template_text = models.TextField()
    field_order_config = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.project_name.title()} - {self.template_name}"
    

