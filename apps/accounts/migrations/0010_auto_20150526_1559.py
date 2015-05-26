# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_subscriptionplan_free_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan',
            name='free_plan',
            field=models.BooleanField(default=False),
        ),
    ]
