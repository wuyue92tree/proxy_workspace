#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):
    list_display = ('source', 'addr', 'port', 'io', 'locate', 'level', 'type',
                    'live_time', 'dateline')
    list_filter = ('source', 'io', 'level', 'type')
    search_fields = ('addr', 'port')


@admin.register(CheckDomain)
class CheckDomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'site', 'check_url', 'status')
    list_filter = ('site__site_name', 'status')
    search_fields = ('domain',)


@admin.register(TargetSite)
class TargetSiteAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'description', 'status')
    list_filter = ('site_name', 'status')
    search_fields = ('site_name',)


@admin.register(ProxyChecked)
class ProxyChecked(admin.ModelAdmin):
    list_display = ('domain', 'proxy', 'get_io', 'get_level', 'get_type',
                    'connect_time', 'check_time')
    list_filter = ('domain__domain', 'domain__site__site_name', 'proxy__io',
                   'proxy__level',
                   'proxy__type')
    search_fields = ('proxy__addr', 'proxy__port')

    def get_io(self, obj):
        if obj.proxy.io == 1:
            return u'国内'
        else:
            return u'国外'
    get_io.admin_order_field = 'id'
    get_io.short_description = '国内/国外'

    def get_level(self, obj):
        if obj.proxy.level == 1:
            return u'透明'
        else:
            return u'高匿'

    get_level.admin_order_field = 'id'
    get_level.short_description = '级别'

    def get_type(self, obj):
        if obj.proxy.type == 1:
            return u'HTTP'
        elif obj.proxy.type == 2:
            return u'HTTPS'
        else:
            return u'HTTP/HTTPS'

    get_type.admin_order_field = 'id'
    get_type.short_description = '类型'
