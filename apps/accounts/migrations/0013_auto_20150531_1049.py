# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_iptracker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iptracker',
            name='view_count',
            field=models.IntegerField(default=0, verbose_name=b'View Count'),
        ),
    ]
