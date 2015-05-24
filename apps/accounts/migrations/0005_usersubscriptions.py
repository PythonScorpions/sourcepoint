# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0004_subscriptionplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSubscriptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(auto_now=True, verbose_name=b'Start Date')),
                ('expiry_date', models.DateTimeField(verbose_name=b'Expiry Date')),
                ('plan', models.ForeignKey(related_name='subscribe_plan', to='accounts.SubscriptionPlan')),
                ('user', models.ForeignKey(related_name='user_plan', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
