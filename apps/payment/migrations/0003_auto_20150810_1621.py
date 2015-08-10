# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='time',
            field=models.TimeField(default=datetime.datetime(2015, 8, 10, 16, 21, 18, 769912, tzinfo=utc), verbose_name=b'Time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(verbose_name=b'Date'),
        ),
    ]
