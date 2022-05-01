# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from myapp.permissions import GenericViewPermission


class UserAPIView(APIView):
    view_group = 'user'
    view_access_permissions = {
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
