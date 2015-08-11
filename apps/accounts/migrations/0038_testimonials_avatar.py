# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0037_testimonials'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonials',
            name='avatar',
            field=models.ImageField(default=1, upload_to=b'banners/', verbose_name=b'Avatar'),
            preserve_default=False,
        ),
    ]
