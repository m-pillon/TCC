from django.urls import path
from . import views

urlpatterns = [
    path('', views.sleep_questionnaire, name='sleep_questionnaire'),
    path('success/', views.questionnaire_success, name='questionnaire_success'),
]