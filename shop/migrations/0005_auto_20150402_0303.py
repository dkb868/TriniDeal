# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_saleitem_dummynumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleitem',
            name='title',
            field=models.CharField(max_length=b'50'),
            preserve_default=True,
        ),
    ]
