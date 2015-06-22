# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20150621_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinterests',
            name='post',
            field=models.ForeignKey(related_name='interest_post', blank=True, to='posts.Posts', null=True),
        ),
        migrations.AlterField(
            model_name='userinterests',
            name='tracker',
            field=models.ForeignKey(related_name='interest_track', blank=True, to='accounts.IpTracker', null=True),
        ),
    ]
