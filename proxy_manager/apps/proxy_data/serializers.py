#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com

from rest_framework import serializers
from .models import Proxy, ProxyChecked


class ProxySerializer(serializers.HyperlinkedModelSerializer):
    io = serializers.SerializerMethodField()

    class Meta:
        model = Proxy
        # fields = '__all__'
        exclude = ('url',)

    def get_io(self, obj):
        if obj.io == 2:
            return u'国外'
        else:
            return u'国内'


class ProxyCheckedSerializer(serializers.HyperlinkedModelSerializer):
    site = serializers.ReadOnlyField(source='site.site')
    proxy = ProxySerializer()

    class Meta:
        model = ProxyChecked
        # fields = '__all__'
        exclude = ('url',)
