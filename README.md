### 功能
视图访问权限控制

1、声明视图访问权限（通过视图类属性view_group、view_access_permissions声明）

2、python manage.py collectpermissions

3、为用户绑定视图权限


### 安装(Install)
> $ pip install django-rest-permission


### 使用(How to use)
项目结构如下
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

1、配置settings.py
```python
INSTALLED_APPS = [
    ...
    'django_rest_permission'
    ...
]
```

2、在permissions.py导入getGenericAPIViewPermission，获取GenericViewPermission

```python
from django_rest_permission.permissions import getGenericViewPermission

GenericViewPermission = getGenericViewPermission()
...
```

3、在views.py导入并使用获取GenericAPIViewPermission
```python
from django.views.generic.base import View
from rest_framework.views import APIView
from myapp.permissions import GenericViewPermission


class MyAPIView01(APIView):
    view_group = '购物车'
    view_access_permissions = {
        'GET': '查询购物车商品',
        'POST': '创建购物车',
        'PUT': '修改购物车商品',
        'DELETE': '清空购物车'
    }
    permission_classes = [GenericViewPermission]
    
    def get(self, request):
        # 业务逻辑
        pass
    
    def post(self, request):
        # 业务逻辑
        pass
    
    ...


class MyView02(View):
    view_group = '用户管理'
    view_access_permissions = {
        'GET': '查询用户信息',
        'POST': '新建用户',
        'PUT': '修改用户资料',
        'DELETE': '删除用户'
    }
    permission_classes = [GenericViewPermission]
    
    def get(self, request):
        # 业务逻辑
        pass
    
    def post(self, request):
        # 业务逻辑
        pass
    
    ...
```

4、权限入库：自动收集已加载的APP中CBV中声明的权限

> 方式1：python manage.py collectpermissions

> 方式2：python manage.py collectpermissions app_name

执行以上命令后，数据库的django_content_type、auth_permission会生成视图对应的权限信息

5、数据库结构 —— django_content_type

| id  | app_label | model |
|-----|-----------|-------|
| 666 | drf_myapp | 购物车   |
| 777 | drf_myapp | 用户管理  |

6、数据库结构 —— auth_permission

| id| name| content_type_id | codename     |
|---|-----|-----------------|--------------------------|
| ... | 查询购物车商品 | 666 | view://myapp/购物车/查询购物车商品 |
| ... | 创建购物车 | 666 | view://myapp/购物车/创建购物车   |
| ... | 修改购物车商品 | 666 | view://myapp/购物车/修改购物车商品 |
| ... | 清空购物车 | 666 | view://myapp/购物车/清空购物车   |
| ... | 查询用户信息 | 777 | view://myapp/用户管理/查询用户信息    |
| ... | 新建用户 | 777 | view://myapp/用户管理/新建用户   |
| ... | 修改用户资料 | 777 | view://myapp/用户管理/修改用户资料 |
| ... | 删除用户 | 777 | view://myapp/用户管理/删除用户   |

7、管理后台创建用户、用户组，并分配权限
