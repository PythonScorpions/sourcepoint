# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0038_testimonials_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonials',
            name='testimonial',
            field=models.TextField(verbose_name=b'Testimonial'),
        ),
    ]
