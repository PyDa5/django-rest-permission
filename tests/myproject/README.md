## 安装依赖(Install requirements)
> pip install -r requirements

## 模型迁移(migrate)
> python manage.py makemigrations
>
> python manage.py migrate

## 视图权限迁移(collectpermissions)
> python manage.py collectpermissions

## 创建超级管理员登陆管理后台(createsuperuser)
    > python manage.py createsuperuser
    > username：admin
    > password：123

## 用管理员账号创建一个普通员工账号(add a staff)
    username: Alex
    password: Django666
    Staff status: √

## 验证视图访问权限配置是否成功(Test)
step1：浏览器打开(http://127.0.0.1:8000/myapp/user?format=json)，Response如下：
   
    {"detail":"Authentication credentials were not provided."}

step2：以Alex身份登陆管理后台(http://127.0.0.1:8000/admin/login/)，在新标签打开(http://127.0.0.1:8000/myapp/user?format=json)，Response如下：
    
    {"detail":"You do not have permission to perform this action."}

step3：以admin省份登陆管理后台(http://127.0.0.1:8000/admin/login/)，为Alex添加权限“user|查询用户信息”，保存，然后在新标签打开(http://127.0.0.1:8000/myapp/user?format=json)，Response如下：
    
    {"msg":"Your request`s method is GET"}

验证通过！

## 注意
* superuser有所有接口的访问权限
