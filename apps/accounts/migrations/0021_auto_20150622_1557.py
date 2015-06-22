# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20150622_1547'),
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
        migrations.RemoveField(
            model_name='userinterests',
            name='post',
        ),
        migrations.RemoveField(
            model_name='userinterests',
            name='tracker',
        ),
        migrations.DeleteModel(
            name='IpTracker',
        ),
        migrations.DeleteModel(
            name='UserInterests',
        ),
    ]
