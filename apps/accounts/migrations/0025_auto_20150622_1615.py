# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20150622_1607'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinterests',
            old_name='post',
            new_name='user_post',
        ),
    ]
