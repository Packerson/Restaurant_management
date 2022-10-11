"""Restaurant_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from Inventory.views import ProductView, ProductAddView, ProductUpdateView, \
    ProductDeleteView, home, login_view, logout_view, add_user_view, CompanyAddView, \
    CompanyListView, CompanyUpdateView, CompanyDelete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='main'),
    path('register/', add_user_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),


    path('product/', ProductView.as_view(), name='product_list'),
    path('product/add/', ProductAddView.as_view(), name='product_add'),
    path('product/<int:pk>/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/delete/<int:pk>', ProductDeleteView.as_view(),
         name='product-delete'),


    path('company/', CompanyListView.as_view(), name='company_list'),
    path('company/add/', CompanyAddView.as_view(), name='company_add'),
    path('company/<int:pk>/', CompanyUpdateView.as_view(), name='company_edit'),
    path('company/delete/<int:pk>', CompanyDelete.as_view(),
         name='company-delete'),

]
