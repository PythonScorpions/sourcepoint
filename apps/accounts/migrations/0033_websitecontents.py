# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('accounts', '0032_subscriptionplan_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebSiteContents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('signin', models.TextField(max_length=150, verbose_name=b'Signin')),
                ('signup', models.TextField(max_length=150, verbose_name=b'Signup')),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
        ),
    ]
