# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_text', models.TextField(max_length=1500)),
                ('comment_time', models.DateField()),
                ('comment_last_edited', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_type', models.CharField(default=b'sell', max_length=4, choices=[(b'buy', b'Buying'), (b'sell', b'Selling')])),
                ('post_text', models.TextField(max_length=1500)),
                ('sale_category', models.CharField(max_length=75)),
                ('post_time', models.DateField()),
                ('post_last_edited', models.DateField()),
                ('price', models.IntegerField()),
                ('availability', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=75)),
                ('seller_points', models.IntegerField(verbose_name=b'concrete measurement of reliability of this person as a seller')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='poster',
            field=models.ForeignKey(to='shop.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(to='shop.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='poster',
            field=models.ForeignKey(to='shop.User'),
            preserve_default=True,
        ),
    ]
