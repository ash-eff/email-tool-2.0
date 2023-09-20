from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomerUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomerUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "project",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("project",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('project', 'email')}),)


admin.site.register(CustomUser, CustomUserAdmin)
