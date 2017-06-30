# -*- coding: utf-8 -*-
from rest_framework import viewsets
from .serializers import ProxySerializer, ProxyCheckedSerializer
from .models import Proxy, ProxyChecked

# Create your views here.


class ProxyViewSet(viewsets.ModelViewSet):
    queryset = Proxy.objects.all().order_by('-dateline')
    serializer_class = ProxySerializer
    filter_fields = ('level', 'type', 'io', 'source')


class ProxyCheckedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProxyChecked.objects.all().order_by('-check_time')
    serializer_class = ProxyCheckedSerializer
    filter_fields = ('domain__domain', 'proxy__io', 'proxy__level',
                     'proxy__type',
                     'proxy__source')
