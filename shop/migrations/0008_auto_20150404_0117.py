# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20150403_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleitem',
            name='deal',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='saleitem',
            name='sale_end_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='saleitem',
            name='usual_price',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
