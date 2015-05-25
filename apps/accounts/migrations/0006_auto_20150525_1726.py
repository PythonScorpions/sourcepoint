# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_usersubscriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofiles',
            name='mobile',
            field=models.IntegerField(null=True, verbose_name=b'Mobile', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='skypeid',
            field=models.CharField(max_length=150, null=True, verbose_name=b'Skype ID', blank=True),
        ),
    ]
