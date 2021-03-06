## 功能(Project description)
若视图继承自djangorestframework的APIView，则此APP可帮助你方便设置用户对视图的访问权限。
```
1、在视图类中声明view_group、view_perms这两个类属性，属性值会对应生成django_content_type、auth_permission的表内容；
2、permission_classes=[GenericViewPermission, ..]，permission_classes中添加GenericViewPermission；
3、执行python manage.py collectpermissions命令，将视图中声明的视图访问权限自动迁移至数据库。
```
好处在于：
```
* 1、method+url级别的权限控制；
* 2、权限声明简单；
* 3、定义的权限自动入库。
```


## 安装(Install)

> pip install django-rest-permission

## 使用(How to use)
####  项目结构如下
```
myproject
    - settings.py
    - urls.py
    - ...
myapp
    - app.py
    - models.py
    - permissions.py(*)
    - urls.py
    - views.py
    - ...
```

#### 1、settings.py
```python
INSTALLED_APPS = [
    ...,
    'rest_framework',
    'django_rest_permission'
]
```

####  2、permissions.py

```python
"""
在APP下的permissions.py导入getGenericViewPermission，获取GenericViewPermission
"""
from django_rest_permission.permissions import getGenericViewPermission

GenericAPIViewPermission = getGenericViewPermission()
...
```

#### 3、views.py
```python
"""
1、导入GenericViewPermission，permission_classes = [permission_classes]
2、视图类中同时声明两个类属性：view_group、view_perms
   view_group 对应数据库django_content_type表的model字段
   view_perms 用于生成数据库auth_permission表的name、codename字段
"""
from rest_framework.views import APIView
from django.views.generic.base import View
from myapp.permissions import GenericViewPermission


class MyAPIView01(APIView):
    # 视图权限分组，对应django_content_type表中的model字段，model = 购物车
    view_group = '购物车'
    # 用于生成auth_permissions中的信息，key-value格式可以是：METHOD: perm_code
    view_perms = {
        'GET': '查询购物车商品',  # name = 查询购物车商品，codename = view://myapp/购物车/查询购物车商品
        'POST': '创建购物车',     # name = 创建购物车， codename = view://myapp/购物车/创建购物车
        'PUT': '修改购物车商品',  # name = 修改购物车商品, codename = view://myapp/购物车/修改购物车商品
        'DELETE': '清空购物车'    # name = 清空购物车， codename = view://myapp/购物/清空购物车
    }
    # 引入权限校验类
    permission_classes = [GenericViewPermission]
    
    def get(self, request):
        # get请求且用户有“查询购物车商品”权限时走这里
        pass
    
    def post(self, request):
        # post请求且用户有“创建购物车”权限时走这里
        pass
    
    ...


class MyView02(View):
    # 视图权限分组，对应django_content_type表中的model字段，model = 用户管理
    view_group = '用户管理'
    # 用于生成auth_permissions中的信息，key-value格式可以是：METHOD: (perm_code, perm_name)
    view_perms = {
        'GET': ('view_user_info', '查询用户信息'),       # name = 查询用户信息, codename = view://myapp/用户管理/view_user_info
        'POST': ('create_user', '新建用户'),             # name = 新建用户, codename = view://myapp/用户管理/create_user
        'PUT': ('modify_user_profile', '修改用户资料'),  # name = 修改用户资料, codename = view://myapp/用户管理/modify_user_profile
        'DELETE': ('delete_user', '删除用户')            # name = 删除用户, codename = view://myapp/用户管理/delete_user
    }
    permission_classes = [GenericViewPermission]
    
    def get(self, request):
        # get请求且用户有“查询用户信息”权限时走这里
        pass
    
    def post(self, request):
        # post请求且用户有“新建用户”权限时走这里
        pass
    ...
```

#### 4、权限入库：自动从已加载的APP中收集在视图类声明的权限

> 方式1：python manage.py collectpermissions

> 方式2：python manage.py collectpermissions app_name

执行以上命令后，数据库的django_content_type、auth_permission会生成视图对应的权限信息

#### 5、django_content_type（自动生成）

| id  | app_label | model |
|-----|-----------|-------|
| 666 | drp_myapp | 购物车   |
| 777 | drp_myapp | 用户管理  |

#### 6、auth_permission（自动生成）

| id| name| content_type_id | codename                 |
|---|-----|-----------------|--------------------------|
| ... | 查询购物车商品 | 666 | view://myapp/购物车/查询购物车商品 |
| ... | 创建购物车 | 666 | view://myapp/购物车/创建购物车   |
| ... | 修改购物车商品 | 666 | view://myapp/购物车/修改购物车商品 |
| ... | 清空购物车 | 666 | view://myapp/购物车/清空购物车   |
| ... | 查询用户信息 | 777 | view://myapp/用户管理/查询用户信息 |
| ... | 新建用户 | 777 | view://myapp/用户管理/新建用户   |
| ... | 修改用户资料 | 777 | view://myapp/用户管理/修改用户资料 |
| ... | 删除用户 | 777 | view://myapp/用户管理/删除用户   |

#### 7、管理后台创建用户、用户组，并分配权限 

例如，当为用户分配“drp_myapp.view://myapp/购物车/清空购物车”权限时，用户就可以通过delete请求方法，访问myapp下MyAPIView01视图中的delete方法。

## 适用范围
* 适用于APIView及其子类
