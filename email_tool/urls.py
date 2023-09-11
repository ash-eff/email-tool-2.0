from django.urls import path
from .views import NoTideAccountView, NoTideEmailTemplateView, home_page, ClearCacheAndCookiesView

urlpatterns = [
    path('', home_page, name='index'),
    path('no-tide-account', NoTideAccountView.as_view(), name='no-tide-account'),
    path('no-tide-email-form-template/<str:name>/', NoTideEmailTemplateView.as_view(), name='no-tide-email-form-template'),
    path('clear-cache-and-cookies/', ClearCacheAndCookiesView.as_view(), name='clear-cache-and-cookies'),
]