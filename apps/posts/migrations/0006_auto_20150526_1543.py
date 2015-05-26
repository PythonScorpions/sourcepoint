# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20150526_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='file',
            field=models.FileField(upload_to=b'files/', null=True, verbose_name=b'File', blank=True),
        ),
    ]
