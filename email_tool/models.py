from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=30)
    no_tide_email_template = models.ForeignKey("EmailTemplate", on_delete=models.CASCADE, null=True, related_name="no_tide")
    clear_cache_and_cookies_email_template = models.ForeignKey("EmailTemplate", on_delete=models.CASCADE, null=True, related_name="clear_cache_and_cookies")

    def __str__(self):
        return self.name

class EmailTemplate(models.Model):
    subject = models.CharField(max_length=100)
    template_text = models.TextField()

    def __str__(self):
        return self.subject
