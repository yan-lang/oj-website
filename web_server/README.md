# Web Server

评测网站的网页服务器，基于Django实现。

## Django Command

```
django-admin makemessages -a
```

## Deployment

部署指南

1. 配置Django项目

```shell script
git clone https://github.com/yan-lang/oj-website.git
cd oj-website/web_server
python manage migrate
python manage.py collectstatic
python manage.py createsuperuser
django-admin compilemessages
```

2. 配置UWSGI

```shell script
pip3 install uwsgi # python2可能会有问题
uwsgi --ini config.ini

uwsgi --reload uwsgi.pid
uwsgi --stop uwsgi.pid

ps -aux | grep uwsgi
ps -aux | grep uwsgi |awk '{print $2}'|xargs kill -9
```

3. 配置Nginx

```shell script
/etc/nginx/sites-enabled/  配置文件路径

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
