# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from myapp.permissions import GenericViewPermission
from myapp.serializers import UserSerializer


class UserAPIView(APIView):
    view_group = 'user'
    view_perms = {
        'GET': ('view_user_info', '查询用户信息'),
        'POST': ('create_user', '新建用户'),
        'PUT': ('modify_user_profile', '修改用户资料'),
        'DELETE': ('delete_user', '删除用户')
    }
    permission_classes = [GenericViewPermission]

    def get(self, req: Request):
        return Response({'msg': 'Your request`s method is GET'})

    def post(self, req: Request):
        return Response({'msg': 'Your request`s method is POST'})

    def delete(self, req: Request):
        return Response({'msg': 'Your request`s method is DELETE'})

    def put(self, req: Request):
        return Response({'msg': 'Your request`s method is PUT'})


class TestModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    view_group = 'resource'
    view_perms = {
        'list': 'list_resources',
        'create': 'create_resource',
        'destroy': 'destroy_resource',
        'retrieve': 'retrieve_resource',
        'update': 'update_resource',
        'partial_update': 'partial_update_resource'
    }
    permission_classes = [GenericViewPermission, ]

    def list(self, request, *args, **kwargs):
        msg = {'msg': f'You already have the permission: {self.view_access_permissions[self.action]}'}
        return Response(msg)

    def create(self, request, *args, **kwargs):
        msg = {'msg': f'You already have the permission: {self.view_access_permissions[self.action]}'}
        return Response(msg)

    def destroy(self, request, *args, **kwargs):
        msg = {'msg': f'You already have the permission: {self.view_access_permissions[self.action]}'}
        return Response(msg)

    def retrieve(self, request, *args, **kwargs):
        msg = {'msg': f'You already have the permission: {self.view_access_permissions[self.action]}'}
        return Response(msg)

    def update(self, request, *args, **kwargs):
        msg = {'msg': f'You already have the permission: {self.view_access_permissions[self.action]}'}
        return Response(msg)

    def partial_update(self, request, *args, **kwargs):
        msg = {'msg': f'You already have the permission: {self.view_access_permissions[self.action]}'}
        return Response(msg)
