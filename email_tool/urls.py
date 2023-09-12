from django.urls import path
from .views import ProjectSelectionView, ProjectLandingPageView, NoTideEmailTemplateView, ClearCacheAndCookiesView, ResetPasswordView

urlpatterns = [
    path('', ProjectSelectionView.as_view(), name='home'),
    path('project-landing-page/<str:name>/', ProjectLandingPageView.as_view(), name='project-landing-page'),
    path('no-tide-email-template/<str:name>/', NoTideEmailTemplateView.as_view(), name='no-tide-email-template'),
    path('clear-cache-and-cookies/<str:name>/', ClearCacheAndCookiesView.as_view(), name='clear-cache-and-cookies'),
    path('reset-password/<str:name>/', ResetPasswordView.as_view(), name='reset-password'),
    path('project-team-escalation/<str:name>/', ResetPasswordView.as_view(), name='project-team-escalation'),
]