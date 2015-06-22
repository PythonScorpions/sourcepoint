# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_postspreview_preview'),
        ('accounts', '0025_auto_20150622_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterestOfUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('ip_tracker', models.ForeignKey(related_name='interest_usertrack', blank=True, to='accounts.IpTracker', null=True)),
                ('post_name', models.ForeignKey(related_name='interest_userpost', blank=True, to='posts.Posts', null=True)),
            ],
        ),
    ]
