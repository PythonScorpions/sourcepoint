# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0014_postspreview_preview'),
        ('accounts', '0021_auto_20150622_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.IPAddressField()),
                ('view_count', models.IntegerField(default=0, verbose_name=b'View Count')),
                ('interest_count', models.IntegerField(default=0, verbose_name=b'Total Interest Shown')),
                ('date', models.DateField(auto_now_add=True)),
                ('posts', models.ManyToManyField(related_name='post_track', to='posts.Posts')),
                ('user', models.ForeignKey(related_name='user_track', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserInterests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(related_name='interest_post', blank=True, to='posts.Posts', null=True)),
                ('tracker', models.ForeignKey(related_name='interest_track', blank=True, to='accounts.IpTracker', null=True)),
            ],
        ),
    ]
