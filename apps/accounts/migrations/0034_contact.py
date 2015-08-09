# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('accounts', '0033_websitecontents'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.BigIntegerField(verbose_name=b'Phone')),
                ('email1', models.EmailField(max_length=254, verbose_name=b'Email1')),
                ('email2', models.EmailField(max_length=254, verbose_name=b'Email2')),
                ('address', models.TextField(verbose_name=b'Address')),
                ('skype', models.CharField(max_length=150, verbose_name=b'Skype')),
                ('fb_link', models.CharField(max_length=150, verbose_name=b'FB Link')),
                ('tw_link', models.CharField(max_length=150, verbose_name=b'FB Link')),
                ('ln_link', models.CharField(max_length=150, verbose_name=b'FB Link')),
                ('youtube_link', models.CharField(max_length=150, verbose_name=b'FB Link')),
                ('googleplus_link', models.CharField(max_length=150, verbose_name=b'FB Link')),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
        ),
    ]
