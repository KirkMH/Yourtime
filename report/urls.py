from django.urls import path
from . import views


urlpatterns = [
    path('due', views.due_report, name='jo_due_report'),
]
