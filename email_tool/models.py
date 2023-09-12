from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=30)
    email_templates = models.ManyToManyField("EmailTemplate")

    def __str__(self):
        return self.name

class EmailTemplate(models.Model):
    subject = models.CharField(max_length=100)
    html_page = models.CharField(max_length=100, default='home')
    template_text = models.TextField()

    def __str__(self):
        return self.subject
