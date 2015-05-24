# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150517_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'Name')),
                ('post_requirement', models.IntegerField(verbose_name=b'Post Requirement')),
                ('view_requirement', models.IntegerField(verbose_name=b'View Requirement')),
                ('view_contact', models.IntegerField(verbose_name=b'View Contact')),
                ('show_interest', models.IntegerField(verbose_name=b'Show Interest')),
                ('contact', models.BooleanField(default=False, verbose_name=b'Displays Contact Detail of Person who Showed Interest')),
            ],
        ),
    ]
