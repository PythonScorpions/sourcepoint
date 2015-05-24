# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20150516_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='buy_code',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='posts',
            name='sell_code',
            field=models.BooleanField(default=False),
        ),
    ]
