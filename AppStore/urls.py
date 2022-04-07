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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.home, name='home'),
    path('register/', app.views.register, name='register'),
    path('profile/<str:id>', app.views.profile, name='profile'),
    path('login/', app.views.signin, name='login'),
    path('logout', app.views.signout, name='logout'),
    path('search_products/', app.views.search_products, name='search_products'),
    path('search_users/', app.views.search_users, name='search_users'),
    path('search/view/<int:id>', app.views.view, name='search/view'),
    path('view/<int:id>', app.views.view, name='view'),
    path('purchase', app.views.purchase, name='purchase'),
    path('sort_top', app.views.sort_top, name='sort_top'),
    path('sort_pricedown', app.views.sort_pricedown, name='sort_pricedown'),
    path('sort_priceup', app.views.sort_priceup, name='sort_priceup')
]
