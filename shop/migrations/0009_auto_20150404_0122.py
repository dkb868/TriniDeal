# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20150404_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleitem',
            name='link',
            field=models.CharField(max_length=b'300', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='saleitem',
            name='offline',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
