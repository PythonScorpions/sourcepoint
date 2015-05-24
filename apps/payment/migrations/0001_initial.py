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
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_type', models.CharField(blank=True, max_length=150, null=True, verbose_name=b'Payment Type', choices=[(b'0', b'Credit Card'), (b'1', b'Paypal')])),
                ('plan', models.CharField(max_length=150, verbose_name=b'Plans')),
                ('amount', models.IntegerField(verbose_name=b'Amount Payed')),
                ('user', models.OneToOneField(related_name='user_payment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
