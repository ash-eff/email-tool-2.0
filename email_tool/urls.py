from django.urls import path, include
from .views import (ProjectSelectionView, ProjectLandingPageView, CreateEmailView, 
                    TemplateBuildView, AdminPanelView, ViewEditTemplateView, EditTemplateView,
                    ProjectAddView, EditSignatureView, FormCreatorView, FormDeleteView, template_delete_confirmation_view,
                    form_delete_confirmation_view, about_view)

urlpatterns = [
    path('', ProjectSelectionView.as_view(), name='home'),
    path('project-landing-page/<str:name>/', ProjectLandingPageView.as_view(), name='project-landing-page'),
    path('email-template/<str:name>/<str:template_name>/', CreateEmailView.as_view(), name='email-template'),
    path('template-builder/<str:name>/', TemplateBuildView.as_view(), name='template-builder'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('admin-panel', AdminPanelView.as_view(), name='admin-panel'),
    path('view-edit-templates/<str:name>/', ViewEditTemplateView.as_view(), name='view-edit-templates'),
    path('edit-template/<str:name>/<slug:template_slug>/', EditTemplateView.as_view(), name='edit-template'),
    path('add-project', ProjectAddView.as_view(), name='add-project'),
    path('edit-signature/<str:name>/', EditSignatureView.as_view(), name='edit-signature'),
    path('form-creator/<str:name>/', FormCreatorView.as_view(), name='form-creator'),
    path('form-delete/<str:name>/', FormDeleteView.as_view(), name='form-delete'),
    path('template_delete_confirmation_view', template_delete_confirmation_view, name='template_delete_confirmation_view'),
    path('form_delete_confirmation_view', form_delete_confirmation_view, name='form_delete_confirmation_view'),
    path('about', about_view, name='about'),

]