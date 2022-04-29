# -*- coding: utf-8 -*-

# 配置auth_permission表中的codename字段格式
PERMISSION_CODENAME_PATTERN = 'view://{app_name}/{view_group}/{permission_code}'

# 配置django_content_type表中的app_label格式
APP_LABEL_PATTERN = 'drf_{app_name}'

# 配置视图权限分组名称
VIEW_GROUP_PROP = 'view_group'

# 配置访问视图所需权限标的属性
VIEW_ACCESS_PERMISSIONS_PROP = 'view_access_permissions'
