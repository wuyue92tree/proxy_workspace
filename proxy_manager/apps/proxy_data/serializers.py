#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from rest_framework import serializers
from .models import Proxy, ProxyChecked
from crwy.spider import Spider

class ProxySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Proxy
        # fields = '__all__'
        exclude = ('url', 'level', 'source', 'io', 'type', 'locate',
                   'live_time', 'dateline')


class ProxyCheckedSerializer(serializers.HyperlinkedModelSerializer):
    domain = serializers.ReadOnlyField(source='domain.domain')
    proxy = ProxySerializer()

    class Meta:
        model = ProxyChecked
        exclude = ('url',)

