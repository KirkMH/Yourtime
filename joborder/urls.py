from django.urls import path
from . import views


urlpatterns = [
    path('', views.jo_list, name='jo_list'),
    path('dt', views.JoDtListView.as_view(), name='jo_dtlist'),
]
