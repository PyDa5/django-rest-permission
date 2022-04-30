# -*- coding: utf-8 -*-
from django.urls import path
from myapp import views

urlpatterns = [
    path('user', views.UserAPIView.as_view())
]
