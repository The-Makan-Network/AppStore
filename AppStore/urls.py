"""AppStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path

import app.views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', app.views.index_products, name='products'), """Home page of the app"""
    path('accounts/login/', auth_views.auth_login, name='login'),
    path('accounts/logout/', auth_views.auth_logout, name='logout'),
    path('view/<str:id>', app.views.view, name='view'),
    path('edit/<str:id>', app.views.edit, name='edit'),
    path('add/', app.views.add, name='add'),
    """path('Admin', app.views.index, name='index'),
    path('buy/', app.views.buy, name='buy'),
    path('login/', app.views.login, name='login'),
    path('purchase/', app.views.purchase, name='purchase'),"""
]
