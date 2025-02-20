"""YourTime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/login/', auth_views.LoginView.as_view(
        template_name='accounts/login-admin.html'), name='login_admin'),
    path('admin/', admin.site.urls),
    path('', include('access.urls')),
    path('client/', include('client.urls')),
    path('joborder/', include('joborder.urls')),
    path('settings/', include('customization.urls')),
    path('reports/', include('report.urls')),
]
