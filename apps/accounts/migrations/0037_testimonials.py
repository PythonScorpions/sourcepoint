# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0036_auto_20150811_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'Name')),
                ('title', models.CharField(max_length=100, verbose_name=b'Title')),
                ('testimonial', models.TextField(max_length=100, verbose_name=b'Testimonial')),
            ],
        ),
    ]
