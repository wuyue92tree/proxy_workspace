# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-30 12:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CheckDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=255, unique=True, verbose_name='\u57df\u540d')),
                ('check_url', models.TextField(blank=True, verbose_name='\u68c0\u6d4b\u94fe\u63a5')),
                ('status', models.BooleanField(default=True, verbose_name='\u662f\u5426\u68c0\u6d4b')),
            ],
            options={
                'verbose_name': '\u57df\u540d\u7ba1\u7406',
                'verbose_name_plural': '\u57df\u540d\u7ba1\u7406',
            },
        ),
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=255, verbose_name='\u6765\u6e90')),
                ('addr', models.CharField(max_length=255, verbose_name='\u5730\u5740')),
                ('port', models.CharField(max_length=255, verbose_name='\u7aef\u53e3')),
                ('io', models.IntegerField(choices=[(1, '\u56fd\u5185'), (2, '\u56fd\u5916')], verbose_name='\u56fd\u5185/\u56fd\u5916')),
                ('locate', models.CharField(max_length=255, verbose_name='\u5730\u533a')),
                ('level', models.IntegerField(choices=[(1, '\u900f\u660e'), (2, '\u9ad8\u533f')], verbose_name='\u7ea7\u522b')),
                ('type', models.IntegerField(choices=[(1, 'HTTP'), (2, 'HTTPS'), (3, 'HTTP/HTTPS')], verbose_name='\u7c7b\u578b')),
                ('live_time', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u5b58\u6d3b\u65f6\u95f4')),
                ('dateline', models.DateTimeField(verbose_name='\u5165\u5e93\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u4ee3\u7406\u6c60',
                'verbose_name_plural': '\u4ee3\u7406\u6c60',
            },
        ),
        migrations.CreateModel(
            name='ProxyChecked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connect_time', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u8fde\u63a5\u65f6\u95f4')),
                ('check_time', models.DateTimeField(blank=True, null=True, verbose_name='\u6700\u540e\u4e00\u6b21\u68c0\u67e5\u65f6\u95f4')),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proxy_data.CheckDomain', verbose_name='\u57df\u540d')),
                ('proxy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proxy_data.Proxy', verbose_name='\u4ee3\u7406')),
            ],
            options={
                'verbose_name': '\u5df2\u68c0\u6d4b\u4ee3\u7406',
                'verbose_name_plural': '\u5df2\u68c0\u6d4b\u4ee3\u7406',
            },
        ),
        migrations.CreateModel(
            name='TargetSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=255, unique=True, verbose_name='\u7ad9\u70b9\u540d\u79f0')),
                ('description', models.TextField(blank=True, verbose_name='\u7ad9\u70b9\u63cf\u8ff0')),
                ('status', models.BooleanField(default=True, verbose_name='\u662f\u5426\u68c0\u6d4b')),
            ],
            options={
                'verbose_name': '\u7ad9\u70b9\u7ba1\u7406',
                'verbose_name_plural': '\u7ad9\u70b9\u7ba1\u7406',
            },
        ),
        migrations.AlterUniqueTogether(
            name='proxy',
            unique_together=set([('addr', 'port', 'type')]),
        ),
        migrations.AddField(
            model_name='checkdomain',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proxy_data.TargetSite', verbose_name='\u6240\u5c5e\u7ad9\u70b9'),
        ),
        migrations.AlterUniqueTogether(
            name='proxychecked',
            unique_together=set([('domain', 'proxy')]),
        ),
    ]