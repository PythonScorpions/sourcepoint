# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_iptracker_interest_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='iptracker',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 6, 5, 15, 47, 9, 206819, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
