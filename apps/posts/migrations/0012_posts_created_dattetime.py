# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_posts_user_contacted'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='created_dattetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 10, 17, 17, 46, 964004, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
