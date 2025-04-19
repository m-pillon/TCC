from django.urls import path
from . import views

urlpatterns = [
    path('', views.sleep_form_view, name='sleep_form'),
    path('success/', views.success_view, name='success'),
]