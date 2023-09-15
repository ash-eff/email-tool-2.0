from django.urls import path
from .views import ProjectSelectionView, ProjectLandingPageView, CreateEmailView, super_secret_one_view, super_secret_two_view

urlpatterns = [
    path('', ProjectSelectionView.as_view(), name='home'),
    path('project-landing-page/<str:name>/', ProjectLandingPageView.as_view(), name='project-landing-page'),
    path('email-template/<str:name>/<str:template_name>/', CreateEmailView.as_view(), name='email-template'),
    path('super-secret-one', super_secret_one_view, name='super-secret-one' ),
    path('super-secret-two', super_secret_two_view, name='super-secret-two' )
]