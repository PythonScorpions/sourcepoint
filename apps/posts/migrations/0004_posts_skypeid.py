# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20150523_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='skypeid',
            field=models.BooleanField(default=False, verbose_name=b'SkypeId'),
        ),
    ]
