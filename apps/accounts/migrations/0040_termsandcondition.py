# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('accounts', '0039_auto_20150811_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsandCondition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(verbose_name=b'Description1')),
                ('description2', models.TextField(verbose_name=b'Description2')),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
        ),
    ]
