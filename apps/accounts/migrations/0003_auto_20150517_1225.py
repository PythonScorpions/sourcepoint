# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userinterests'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofiles',
            name='otp',
            field=models.IntegerField(null=True, verbose_name=b'OTP', blank=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='token',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Token', blank=True),
        ),
    ]
