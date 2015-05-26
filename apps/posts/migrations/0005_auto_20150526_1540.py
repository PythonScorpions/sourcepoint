# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_posts_skypeid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='file',
            field=models.FileField(upload_to=b'files/', null=True, verbose_name=b'File'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='prices',
            field=models.CharField(max_length=150, verbose_name=b'Prices', choices=[(b'1', b'< $10'), (b'2', b'$10 to $50'), (b'3', b'$50 to $100'), (b'4', b'$100 to 200'), (b'5', b'$200 to $300'), (b'6', b'$300 to $500'), (b'7', b'$500 to $750'), (b'8', b'$750 to $1000'), (b'9', b'$1000 to $5000'), (b'10', b'Not Fixed')]),
        ),
    ]
