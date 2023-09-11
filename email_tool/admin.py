from django.contrib import admin
from django.db import models
from .models import Project, EmailTemplate

class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    search_fields = ('subject',)
    formfield_overrides = {
        models.TextField: {'widget': admin.widgets.AdminTextareaWidget(attrs={'rows': 10, 'cols': 60})}
    }


admin.site.register(Project)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
