# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20150810_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='time',
            field=models.TimeField(auto_now_add=True, verbose_name=b'Time'),
        ),
    ]
