# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20150525_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofiles',
            name='email_verify',
            field=models.BooleanField(default=False, verbose_name=b'Email Verified'),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='mobile_verify',
            field=models.BooleanField(default=False, verbose_name=b'Mobile Verified'),
        ),
    ]
