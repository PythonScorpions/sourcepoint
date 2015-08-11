# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0035_auto_20150811_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aboutus',
            name='testimonial',
        ),
        migrations.RemoveField(
            model_name='aboutus',
            name='testimonial2',
        ),
        migrations.RemoveField(
            model_name='aboutus',
            name='testimonial3',
        ),
        migrations.AddField(
            model_name='ourtema',
            name='testimonial',
            field=models.TextField(default=1, verbose_name=b'Client Testimonial1'),
            preserve_default=False,
        ),
    ]
