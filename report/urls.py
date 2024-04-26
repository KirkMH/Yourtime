from django.urls import path
from . import views


urlpatterns = [
    path('due', views.due_report, name='jo_due_report'),
    path('clients', views.client_report, name='client_report'),
    path('job_order/<int:pk>/<str:type>',
         views.job_order, name='generate_job_order'),
]
