from django.urls import path
from . import views

urlpatterns = [
    path('whatsapp/', views.whatsapp_webhook, name='whatsapp_webhook'),
    path('health/', views.health_check, name='health_check'),
]
