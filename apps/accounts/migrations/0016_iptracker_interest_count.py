# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20150604_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='iptracker',
            name='interest_count',
            field=models.IntegerField(default=0, verbose_name=b'Total Interest Shown'),
        ),
    ]
