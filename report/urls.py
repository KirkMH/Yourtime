from django.urls import path
from . import views


urlpatterns = [
    path('due', views.due_report, name='jo_due_report'),
    path('clients', views.client_report, name='client_report'),
    path('job_order/<int:pk>/<str:type>',
         views.job_order, name='generate_job_order'),
    path('technicians', views.technician_metrics, name='tech_metrics'),
    path('collections/summary', views.collections_summary,
         name='collections_summary'),
    path('collections/detailed', views.collections_detailed,
         name='collections_detailed'),
    path('receivables', views.accounts_receivables,
         name='receivables'),
]
