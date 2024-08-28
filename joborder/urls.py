from django.urls import path
from . import views


urlpatterns = [
    path('', views.jo_list, name='jo_list'),
    path('dt', views.JoDtListView.as_view(), name='jo_dtlist'),
    path('create', views.create_jo, name='create_jo'),
    path('<int:pk>/create', views.create_jo_from_client,
         name='create_jo_from_client'),  # pk is client id
    path('<int:pk>/detail', views.JobOrderDetailView.as_view(), name='jo_details'),
    path('<int:pk>/watch/add', views.JobOrderWatchCreateView.as_view(),
         name='jo_watch_add'),   # pk is the job order id
    path('<int:pk>/detail/edit', views.JobOrderDetailUpdateView.as_view(),
         name='jo_detail_edit'),   # pk is either the watch id, job order id, assessment id
    path('<int:pk>/estimate/save', views.save_estimate, name='jo_save_estimate'),
    path('<int:pk>/documentation/add', views.JobOrderDocumentationCreateView.as_view(),
         name='jo_documentation_add'),   # pk is the job order id
    path('<int:pk>/status', views.update_jo_status, name='update_jo_status'),
    # pk is photo id, type is either arrival or release
    path('photos/<str:type>/<int:pk>/delete',
         views.delete_photo, name='delete_photo'),
]
