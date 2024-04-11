from django.urls import path
from . import views


urlpatterns = [
    path('', views.setting_list, name='setting_list'),
    path('dt', views.SettingDTListView.as_view(), name='setting_dtlist'),
    path('new', views.SettingCreateView.as_view(), name='new_setting_item'),
    path('<int:pk>/edit', views.SettingUpdateView.as_view(),
         name='edit_setting_item'),
]
