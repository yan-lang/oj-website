https://stackoverflow.com/questions/22470637/django-show-validationerror-in-template

https://wsvincent.com/django-user-authentication-tutorial-password-reset/

https://github.com/django/django/tree/master/django/contrib/admin/templates/registration


## Deployment

```shell script
python manage.py collectstatic
```

```shell script
uwsgi --chdir /home/ubuntu/oj-website --module website.wsgi:application --home /home/ubuntu/django/ --http :8888

uwsgi --reload xxx.pid
uwsgi --stop xxx.pid

ps -aux | grep uwsgi
ps -aux | grep uwsgi |awk '{print $2}'|xargs kill -9
```

**nginx**

```shell script
ps -ef|grep -i nginx

nginx -t  # 检查nginx语法问题

/etc/init.d/nginx start  #启动
/etc/init.d/nginx stop  #关闭
/etc/init.d/nginx restart  #重启
killall nginx    杀死所有nginx

# 如果是生产环境的话Nginx正在运行，就不要直接stop start 或者 restart  直接reload就行了
# 对线上影响最低
/etc/init.d/nginx reload
```

- https://uwsgi.readthedocs.io/en/latest/tutorials/Django_and_nginx.html
- http://www.chenxm.cc/article/87.html
- https://www.zhihu.com/question/54982081/answer/656763472

**Http ~ Https**

```
server {
    listen 80;
    server_name zeqianglai.com www.zeqianglai.cn;
    return 301 https://$server_name$request_uri;
}
```

```python
class MixedPermissionModelViewSet(viewsets.ModelViewSet):
    """
    Mixed permission base model allowing for action level
    permission control. Subclasses may define their permissions
    by creating a 'permission_classes_by_action' variable.

    Example:
    permission_classes_by_action = {'list': [AllowAny],
                                    'create': [IsAdminUser]}
    """

    permission_classes_by_action = {}

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

```