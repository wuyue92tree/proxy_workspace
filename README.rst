proxy_workspace
=================================================

免费IP代理平台

实现原理
=================================================

- 执行proxy_spider内置的爬虫，抓取网站免费代理；
- 通过proxy_manager写入待检测网站链接；
- 执行proxy_spider内置的爬虫检测代理有效性；
- 通过restful接口读取数据库中的代理地址。

运行环境
=================================================

 * Python2.7
 * Works on Linux, Mac OSX

依赖包
=================================================
 * Crwy>=1.0.5
 * Django>=1.10.5
 * django-filter>=1.0.1
 * django-suit>=0.2.23
 * djangorestframework>=3.5.3
 * docutils>=0.13.1
 * redis>=2.10.5
 * SQLAlchemy>=1.1.4

初始化proxy_manager
=================================================

- 进入proxy_manager目录；
- python manage.py makemigrations;
- python manage.py migrate;
- 添加超级管理员账户：python manage.py createsuperuser;
- python manage.py runserver
- 访问：http://localhost:8000

执行爬虫proxy_spider
=================================================

- 抓取免费西刺代理：crwy runspider -n proxy xici;
- 抓取免费快代理：crwy runspider -n proxy kuai;
- 检测代理有效性：crwy runspider -n check;

注意事项
=================================================

 1. 爬虫检测时依赖于redis服务器，请自行安装；
 2. 可将爬虫爬取和检测设置为定时任务，请自行脑补^_^。

修改日志
===================

2017-06-23

- 调整代理获取整体结构/检测代理接口暂时停止使用。