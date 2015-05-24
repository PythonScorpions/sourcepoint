# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'Category')),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150, verbose_name=b'Post Title')),
                ('description', models.TextField(verbose_name=b'Description')),
                ('file', models.FileField(upload_to=b'files/', verbose_name=b'File')),
                ('mobile', models.BooleanField(default=False, verbose_name=b'Hide Mobile')),
                ('prices', models.CharField(max_length=150, verbose_name=b'Prices', choices=[(b'1', b'< $10'), (b'2', b'$10 to $50'), (b'3', b'$50 to $100'), (b'4', b'$100 to 200'), (b'5', b'$200 to $300'), (b'6', b'$300 to $500'), (b'7', b'$500 to $750'), (b'8', b'$750 to $1000'), (b'9', b'$1000 to $5000')])),
                ('email', models.BooleanField(default=False, verbose_name=b'Hide Email')),
                ('created_date', models.DateField(auto_now=True, verbose_name=b'Created Date')),
                ('expiry_date', models.DateField(null=True, verbose_name=b'Expiry Date', blank=True)),
                ('category', models.ForeignKey(to='posts.Category')),
                ('user', models.ForeignKey(related_name='user_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
