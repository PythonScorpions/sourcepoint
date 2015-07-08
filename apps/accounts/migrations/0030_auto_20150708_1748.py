# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_iptracker_post_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscriptions',
            name='post_requirement',
            field=models.IntegerField(default=1, verbose_name=b'Post Requirement'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usersubscriptions',
            name='show_interest',
            field=models.IntegerField(default=1, verbose_name=b'Show Interest'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usersubscriptions',
            name='view_contact',
            field=models.IntegerField(default=1, verbose_name=b'View Contact'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usersubscriptions',
            name='view_requirement',
            field=models.IntegerField(default=1, verbose_name=b'View Requirement'),
            preserve_default=False,
        ),
    ]
