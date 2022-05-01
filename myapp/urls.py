# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.routers import DefaultRouter
from myapp import views

router = DefaultRouter()
router.register('resource', views.TestModelViewSet)

urlpatterns = [
    path('user', views.UserAPIView.as_view())
]
urlpatterns += router.urls
