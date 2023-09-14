from django.urls import path
from .views import ProjectSelectionView, ProjectLandingPageView, CreateEmailView

urlpatterns = [
    path('', ProjectSelectionView.as_view(), name='home'),
    path('project-landing-page/<str:name>/', ProjectLandingPageView.as_view(), name='project-landing-page'),
    path('email-template/<str:name>/<str:email_subject>/', CreateEmailView.as_view(), name='email-template'),
]