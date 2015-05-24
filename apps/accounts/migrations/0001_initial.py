# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mobile', models.IntegerField(verbose_name=b'Mobile')),
                ('skypeid', models.CharField(max_length=150, verbose_name=b'Skype ID')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('smsalert', models.BooleanField(default=False, verbose_name=b'Sms Alert')),
                ('emailalert', models.BooleanField(default=False, verbose_name=b'Email Alert')),
                ('user', models.OneToOneField(related_name='user_profiles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
            },
        ),
    ]
