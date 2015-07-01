# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_contactsviewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='price',
            field=models.IntegerField(default=0, verbose_name=b'Price'),
        ),
    ]
