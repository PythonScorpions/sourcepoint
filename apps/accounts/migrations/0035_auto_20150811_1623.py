# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='testimonial2',
            field=models.TextField(default=1, verbose_name=b'Client Testimonial2'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aboutus',
            name='testimonial3',
            field=models.TextField(default=1, verbose_name=b'Client Testimonial3'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='testimonial',
            field=models.TextField(verbose_name=b'Client Testimonial1'),
        ),
    ]
