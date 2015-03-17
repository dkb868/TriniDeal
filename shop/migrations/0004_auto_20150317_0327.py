# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20150317_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbid',
            name='message',
            field=models.CharField(max_length=b'50', blank=True),
            preserve_default=True,
        ),
    ]
