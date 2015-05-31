# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20150526_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinterests',
            name='interests',
        ),
        migrations.RemoveField(
            model_name='userinterests',
            name='user',
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='contact_viewes',
            field=models.BigIntegerField(null=True, verbose_name=b'Total Contact Viewes', blank=True),
        ),
        migrations.DeleteModel(
            name='UserInterests',
        ),
    ]
