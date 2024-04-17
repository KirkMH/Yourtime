from django.urls import path
from . import views


urlpatterns = [
    path('', views.overdue_report, name='jo_overdue_report'),
]
