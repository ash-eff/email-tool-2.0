from django.urls import path, include
from .views import ProjectSelectionView, ProjectLandingPageView, CreateEmailView, TemplateBuildView, AdminPanelView

urlpatterns = [
    path('', ProjectSelectionView.as_view(), name='home'),
    path('project-landing-page/<str:name>/', ProjectLandingPageView.as_view(), name='project-landing-page'),
    path('email-template/<str:name>/<str:template_name>/', CreateEmailView.as_view(), name='email-template'),
    path('template-builder/<str:name>/', TemplateBuildView.as_view(), name='template-builder'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('admin-panel', AdminPanelView.as_view(), name='admin-panel'),
]