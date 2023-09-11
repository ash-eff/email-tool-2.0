from django.urls import path
from .views import NoTideAccountView, EmailTemplateView, home_page

urlpatterns = [
    path('', home_page, name='index'),
    path('no-tide-account', NoTideAccountView.as_view(), name='no-tide-account'),
    path('email-form-template/<str:name>/', EmailTemplateView.as_view(), name='email-form-template'),
    #path('generated-email/<str:selected_project>/', generated_email, name='generated-email')
]