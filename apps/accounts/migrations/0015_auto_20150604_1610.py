# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_posts_user_contacted'),
        ('accounts', '0014_iptracker_interest_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iptracker',
            name='interest_count',
        ),
        migrations.AddField(
            model_name='iptracker',
            name='intersets',
            field=models.ManyToManyField(to='posts.Posts', null=True, blank=True),
        ),
    ]
