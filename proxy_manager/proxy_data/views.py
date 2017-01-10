# -*- coding: utf-8 -*-
from rest_framework import viewsets
from .serializers import ProxySerializer, ProxyCheckedSerializer
from .models import Proxy, ProxyChecked

# Create your views here.


class ProxyViewSet(viewsets.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer
    filter_fields = ('level', 'type', 'io')


class ProxyCheckedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProxyChecked.objects.all()
    serializer_class = ProxyCheckedSerializer
    filter_fields = ('site', 'proxy__io', 'proxy__level', 'proxy__type')
