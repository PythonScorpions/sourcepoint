# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_subscriptionplan_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='iptracker',
            name='post_count',
            field=models.IntegerField(default=0, verbose_name=b'Total Post Added'),
        ),
    ]
