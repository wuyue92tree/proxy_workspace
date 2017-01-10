from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):
    list_display = ('addr', 'port', 'io', 'locate', 'level', 'type',
                    'live_time', 'dateline')
    list_filter = ('io', 'level', 'type')
    search_fields = ('addr', 'port')


@admin.register(TargetSite)
class TargetSiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'site', 'site_name', 'status')


@admin.register(ProxyChecked)
class ProxyChecked(admin.ModelAdmin):
    list_display = ('site', 'proxy', 'connect_time', 'check_time')
    list_filter = ('site__site_name',)
