# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20150402_0303'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleitem',
            name='dummyfacebook',
            field=models.CharField(max_length=b'200', blank=True),
            preserve_default=True,
        ),
    ]
