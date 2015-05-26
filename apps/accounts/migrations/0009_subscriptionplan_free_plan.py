# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20150526_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='free_plan',
            field=models.BooleanField(default=True),
        ),
    ]
