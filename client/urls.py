from django.urls import path
from . import views


urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('dt', views.ClientDTListView.as_view(), name='client_dtlist'),
    path('new', views.ClientCreateView.as_view(), name='new_client'),
    path('<int:pk>/edit',
         views.ClientUpdateView.as_view(), name='edit_client'),
    path('<int:pk>/detail',
         views.ClientDetailView.as_view(), name='client_detail'),

    path('portal', views.portal_list, name='portal_list'),
    path('portal/dt', views.PortalDTListView.as_view(), name='portal_dtlist'),
    path('portal/<int:pk>/delete',
         views.portalDeleteView, name='portal_delete'),
]
