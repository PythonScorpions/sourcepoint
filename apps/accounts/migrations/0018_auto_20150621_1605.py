# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_iptracker_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iptracker',
            name='intersets',
        ),
        migrations.RemoveField(
            model_name='iptracker',
            name='posts',
        ),
        migrations.RemoveField(
            model_name='iptracker',
            name='user',
        ),
        migrations.DeleteModel(
            name='IpTracker',
        ),
    ]
