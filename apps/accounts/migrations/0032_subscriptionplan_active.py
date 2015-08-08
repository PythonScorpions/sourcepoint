# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_aboutus_ourtema'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='active',
            field=models.BooleanField(default=True, verbose_name=b'Active'),
        ),
    ]
