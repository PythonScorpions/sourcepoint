# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('accounts', '0040_termsandcondition'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('daily_report', models.FileField(null=True, upload_to=b'files/', blank=True)),
                ('monthly_report', models.FileField(null=True, upload_to=b'files/', blank=True)),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
        ),
    ]
