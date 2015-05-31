# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0011_posts_user_contacted'),
        ('accounts', '0011_auto_20150531_0943'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.IPAddressField()),
                ('view_count', models.IntegerField(verbose_name=b'View Count')),
                ('posts', models.ManyToManyField(related_name='post_track', to='posts.Posts')),
                ('user', models.ForeignKey(related_name='user_track', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
