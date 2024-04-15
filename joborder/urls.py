from django.urls import path
from . import views


urlpatterns = [
    path('', views.jo_list, name='jo_list'),
    path('dt', views.JoDtListView.as_view(), name='jo_dtlist'),
    path('create', views.create_jo, name='create_jo'),
    path('<int:pk>/detail', views.JobOrderDetailView.as_view(), name='jo_details'),
    path('<int:pk>/watch/add', views.JobOrderWatchCreateView.as_view(),
         name='jo_watch_add'),   # pk is the job order id
    path('<int:pk>/detail/edit', views.JobOrderDetailUpdateView.as_view(),
         name='jo_detail_edit'),   # pk is either the watch id or job order id
    path('<int:pk>/estimate/save', views.save_estimate, name='jo_save_estimate'),
]
