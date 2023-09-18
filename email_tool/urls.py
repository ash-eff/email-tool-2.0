from django.urls import path
from .views import ProjectSelectionView, ProjectLandingPageView, CreateEmailView, TemplateBuildView

urlpatterns = [
    path('', ProjectSelectionView.as_view(), name='home'),
    path('project-landing-page/<str:name>/', ProjectLandingPageView.as_view(), name='project-landing-page'),
    path('email-template/<str:name>/<str:template_name>/', CreateEmailView.as_view(), name='email-template'),
    path('template-builder/<str:name>/', TemplateBuildView.as_view(), name='template-builder' )
]