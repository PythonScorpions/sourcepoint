# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20150526_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='publish',
            field=models.BooleanField(default=False),
        ),
    ]
