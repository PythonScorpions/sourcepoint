# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('accounts', '0030_auto_20150708_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('banner', models.ImageField(upload_to=b'banners/')),
                ('description', models.TextField(verbose_name=b'Company Overview')),
                ('testimonial', models.TextField(verbose_name=b'Client Testimonial')),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
        ),
        migrations.CreateModel(
            name='OurTema',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.ImageField(upload_to=b'images/')),
                ('name', models.CharField(max_length=150, verbose_name=b'Name')),
                ('title', models.CharField(max_length=150, verbose_name=b'Title')),
                ('description', models.TextField(verbose_name=b'Description')),
            ],
        ),
    ]
