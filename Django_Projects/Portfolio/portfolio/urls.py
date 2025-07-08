from django.urls import path
from .views import (
    HomeView, AboutView, 
    ProjectsView, ResumeView, 
    contact_view
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('resume/', ResumeView.as_view(), name='resume'),
    path('contact/', contact_view, name='contact'),
]