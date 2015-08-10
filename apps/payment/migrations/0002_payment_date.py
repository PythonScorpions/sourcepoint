# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 10, 15, 39, 53, 504302, tzinfo=utc), verbose_name=b'Date & Time'),
            preserve_default=False,
        ),
    ]
