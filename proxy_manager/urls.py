"""proxy_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/admin/')),
    url(r'^admin/', admin.site.urls),
    url(r'^proxy_data/', include("proxy_manager.apps.proxy_data.urls",
                                 namespace='proxy_data')),
    url(r'^docs/', include_docs_urls(title='My API title'))
]
