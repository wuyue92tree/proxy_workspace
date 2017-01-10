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
 * beautifulsoup4>=4.5.3
 * certifi>=2016.9.26
 * configparser>=3.5.0
 * Crwy>=1.0.2
 * Django>=1.10.5
 * django-filter>=1.0.1
 * django-suit>=0.2.23
 * djangorestframework>=3.5.3
 * docutils>=0.13.1
 * pycurl>=7.43.0
 * redis>=2.10.5
 * SQLAlchemy>=1.1.4
 * tqdm>=4.10.0

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

- 抓取免费代理：crwy runspider -n proxy get;
- 检测代理有效性：crwy runspider -n check;

注意事项
=================================================

 1. 爬虫检测时依赖于redis服务器，请自行安装；
 2. 可将爬虫爬取和检测设置为定时任务，请自行脑补^_^。
