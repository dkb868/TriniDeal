# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20150402_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleitem',
            name='dummynumber',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
