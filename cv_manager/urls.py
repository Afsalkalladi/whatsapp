"""
URL configuration for CV Manager project.
"""
from django.urls import path, include

urlpatterns = [
    path('webhook/', include('webhook.urls')),
]
