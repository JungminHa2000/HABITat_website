"""HABITat_website URL Configuration

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
from django.urls import include, path
from django.views.generic.base import TemplateView
from . import views


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='Registration/login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('homepage/', TemplateView.as_view(template_name='webHome.html'), name='homepage'),
    path('reports/', views.all_reports, name='all_reports'),
    path('requests/', views.all_requests, name='all_requests'),
    path('delete/<int:req_id>/', views.decline_request, name='delete'),
    path('accept/<int:req_id>/', views.accept_request, name='accept'),
    path('delete_rep/<int:rep_id>/', views.decline_report, name='delete_rep'),
    path('accept_rep/<int:rid>/', views.accept_report, name ='accept_rep'),
    path('show_all_users/', views.show_all_users, name='show_all_users'),
]
