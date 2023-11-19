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
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('vis/', views.visualisation, name='vis'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('homepage/', views.home_summary, name='homepage'),
    path('reports/', views.all_reports, name='all_reports'),
    path('reports/<str:reportee>/', views.get_reportee_reports, name='reportee_reports'),
    path('requests/', views.all_requests, name='all_requests'),
    path('delete/<int:req_id>/', views.decline_request, name='delete'),
    path('accept/<int:req_id>/', views.accept_request, name='accept'),
    path('delete_rep/<int:rep_id>/', views.decline_report, name='delete_rep'),
    path('accept_rep/<int:rep_id>/', views.accept_report, name ='accept_rep'),
    path('show_all_users/', views.show_all_users, name='show_all_users'),
    path('user_info/<int:user_id>/', views.user_info, name='user_info'),
    path('delete_user/<int:uid>/', views.delete_user, name='delete_user'),
]
