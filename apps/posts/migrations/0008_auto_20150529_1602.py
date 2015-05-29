# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_posts_publish'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posts',
            options={'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=1, populate_from=b'name', editable=False),
            preserve_default=False,
        ),
    ]
