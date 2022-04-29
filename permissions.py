# -*- coding: utf-8 -*-
"""
视图权限入库
python manage.py collectpermissions
python manage.py collectpermissions app_name
"""

import inspect
from importlib import import_module
from os.path import dirname, basename, join, exists

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.views.generic.base import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from django_rest_permission.settings import VIEW_GROUP_PROP, VIEW_ACCESS_PERMISSIONS_PROP, APP_LABEL_PATTERN

User = get_user_model()


class _GenericViewPermission(BasePermission):
    """
    视图级别的权限控制，在视图类中定义view_group和view_access_permissions来声明访问视图所需要的权限
    :view_group 在视图中定义的属性，表示权限分组名称（必须）
    :view_access_permissions 在视图中定义的属性，用于表示请求方法对应的权限名称映射关系，取值例如：
                            1、{'GET': (perm_code, perm_name), 'POST': (perm_code, perm_name),...}
                            2、{'GET': perm_code, 'POST': perm_code,...}，value为字符串时，perm_name=perm_code
    """
    allowed_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

    def has_permission(self, request: Request, view: View):
        """
        根据请求方法和
        """
        method = request.method                         # 获取请求方法
        user: User = request.user                       # 获取当前用户
        user_permissions = user.get_user_permissions()  # 获取用户权限
        app_name = self.app_name                        # 当前视图所在APP名称

        # 视图不包含分组名称和访问权限说明属性的，不做权限校验
        if not (hasattr(view, VIEW_GROUP_PROP) and hasattr(view, VIEW_ACCESS_PERMISSIONS_PROP)):
            return True
        view_group = getattr(view, VIEW_GROUP_PROP)                             # 视图名称(对应django_content_type中的model名称)
        view_access_permissions = getattr(view, VIEW_ACCESS_PERMISSIONS_PROP)   # 映射：请求方法 ==> 权限名称

        # 除了allowed_methods中的方法，其它请求方法不做限制
        if method not in self.allowed_methods:
            return super().has_permission(request, view)

        # 匿名用户不许登陆
        if isinstance(user, AnonymousUser):
            return False

        # 不存在用户权限不允许访问
        if not user_permissions:
            return False

        # 当前请求所需权限
        if method not in view_access_permissions:
            return False

        # 期望的权限名称
        if type(view_access_permissions[method]) == str:
            perm_code = view_access_permissions[method]
        else:
            perm_code, perm_name = view_access_permissions[method]
        expected_permission = APP_LABEL_PATTERN.format(
            app_name=app_name) + '.' + f'view://{app_name}/{view_group}/{perm_code}'
        if expected_permission in user_permissions:
            return True
        return False


def getGenericViewPermission():
    """
    返回GenericViewPermission
    """
    previous_frame = inspect.currentframe().f_back
    filename, line_number, function_name, lines, index = inspect.getframeinfo(previous_frame)
    # 获取调用方app.py所在的包名
    fp = filename
    current_dir_path = dirname(fp)
    current_dir_name = basename(current_dir_path)
    while not (exists(join(current_dir_path, '__init__.py')) and exists(join(current_dir_path, 'apps.py'))):
        fp = current_dir_path
        current_dir_path = dirname(fp)
        current_dir_name = basename(current_dir_path)
    caller_package_name = current_dir_name
    try:
        module = import_module(f'{caller_package_name}.apps')
        ApiConfig = getattr(module, 'ApiConfig')
    except:
        ImportError('请在app目录下的permissions.py中导入此模块')
    app_name = getattr(ApiConfig, 'name')
    klass = _GenericViewPermission
    klass.app_name = app_name
    return klass
