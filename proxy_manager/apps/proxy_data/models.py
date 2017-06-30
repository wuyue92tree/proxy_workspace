#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from __future__ import unicode_literals

from django.db import models


class Proxy(models.Model):
    IO_CHOICE = (
        (1, '国内'),
        (2, '国外')
    )
    LEVEL_CHOICE = (
        (1, '透明'),
        (2, '高匿')
    )
    TYPE_CHOICE = (
        (1, 'HTTP'),
        (2, 'HTTPS'),
        (3, 'HTTP/HTTPS'),
    )
    source = models.CharField(max_length=255, verbose_name='来源')
    addr = models.CharField(max_length=255, verbose_name='地址')
    port = models.CharField(max_length=255, verbose_name='端口')
    io = models.IntegerField(choices=IO_CHOICE, verbose_name='国内/国外')
    locate = models.CharField(max_length=255, verbose_name='地区')
    level = models.IntegerField(choices=LEVEL_CHOICE, verbose_name='级别')
    type = models.IntegerField(choices=TYPE_CHOICE, verbose_name='类型')
    live_time = models.CharField(max_length=255, blank=True, null=True,
                                 verbose_name='存活时间')
    dateline = models.DateTimeField(verbose_name='入库时间')

    def __unicode__(self):
        return self.addr+':'+self.port

    class Meta:
        unique_together = (('addr', 'port', 'type'),)
        verbose_name = "代理池"
        verbose_name_plural = verbose_name


class TargetSite(models.Model):
    site_name = models.CharField(max_length=255, unique=True,
                                 verbose_name='站点名称')
    description = models.TextField(blank=True, verbose_name='站点描述')
    status = models.BooleanField(default=True, verbose_name='是否检测')

    def __unicode__(self):
        return self.site_name

    class Meta:
        verbose_name = "站点管理"
        verbose_name_plural = verbose_name


class CheckDomain(models.Model):
    domain = models.CharField(max_length=255, unique=True, verbose_name='域名')
    site = models.ForeignKey(TargetSite, verbose_name='所属站点')
    check_url = models.TextField(blank=True, verbose_name='检测链接')
    status = models.BooleanField(default=True, verbose_name='是否检测')

    def __unicode__(self):
        return self.domain

    class Meta:
        verbose_name = "域名管理"
        verbose_name_plural = verbose_name


class ProxyChecked(models.Model):
    domain = models.ForeignKey('CheckDomain', verbose_name='域名')
    proxy = models.ForeignKey('Proxy', verbose_name='代理')
    connect_time = models.CharField(max_length=20, blank=True, null=True,
                                    verbose_name='连接时间')
    check_time = models.DateTimeField(blank=True, null=True,
                                      verbose_name='最后一次检查时间')

    class Meta:
        unique_together = (('domain', 'proxy'),)
        verbose_name = "已检测代理"
        verbose_name_plural = verbose_name
