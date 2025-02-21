from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search', views.search_page, name='search'),
    path('', views.dashboard, name='dashboard'),
    path('credentials', views.changeCredentials, name='change_credentials'),

    path('employees', views.EmployeeList.as_view(), name='employee_list'),
    path('employees/new', views.employeeCreate, name='new_employee'),
    path('employees/<int:pk>/reset',
         views.resetPassword, name='employee_reset'),
    path('employees/<int:pk>/remove',
         views.removeAsUser, name='employee_remove'),
    path('employees/<int:pk>/add',
         views.addAsUser, name='employee_add'),
    path('employees/<int:pk>/update',
         views.employeeUpdate, name='employee_update'),
    path('employees/<int:pk>/delete',
         views.employeeDelete, name='employee_delete'),
]
