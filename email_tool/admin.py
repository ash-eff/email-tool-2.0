from django.contrib import admin
from django.db import models
from .models import Project, CustomFormField, CustomFormTemplate, CustomFormSignature


admin.site.register(Project)
admin.site.register(CustomFormTemplate)
admin.site.register(CustomFormField)
admin.site.register(CustomFormSignature)