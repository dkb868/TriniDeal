# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20150330_0046'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleitem',
            name='dummydelivery',
            field=models.CharField(max_length=b'40', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='saleitem',
            name='dummylocation',
            field=models.CharField(max_length=b'40', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='saleitem',
            name='dummyseller',
            field=models.CharField(max_length=b'40', blank=True),
            preserve_default=True,
        ),
    ]
