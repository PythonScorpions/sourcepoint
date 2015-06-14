# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_postspreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='postspreview',
            name='preview',
            field=models.ForeignKey(related_name='post_preview', blank=True, to='posts.Posts', null=True),
        ),
    ]
