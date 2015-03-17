# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20150317_0246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='saleitem',
            old_name='availability',
            new_name='available',
        ),
    ]
