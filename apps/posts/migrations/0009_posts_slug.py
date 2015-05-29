# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20150529_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=1, populate_from=b'title', editable=False),
            preserve_default=False,
        ),
    ]
