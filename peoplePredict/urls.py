# -*-coding:utf-8 -*-
"""peoplePredict URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from peoplePredict.view import model_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('example/', model_view.predict),
    path('api/get_map_data/', model_view.get_map_data),
    path('api/get_radius_data/', model_view.get_radius_data),
    path('api/get_point_data/', model_view.get_point_data),
    path('api/get_top_ten_street/', model_view.get_top_ten_street),
    path('api/get_all_district/', model_view.get_all_district),
    path('api/get_district_point/', model_view.get_district_point),
    path('api/get_district_treemap/', model_view.get_district_treemap)
]
