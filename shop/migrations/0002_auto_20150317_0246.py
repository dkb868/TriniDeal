# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=b'20')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=b'30')),
                ('description', models.TextField(max_length=b'200', blank=True)),
                ('asking_price', models.IntegerField(default=0)),
                ('negotiable', models.BooleanField(default=True)),
                ('expiration_date', models.DateField(null=True, blank=True)),
                ('availability', models.BooleanField(default=True)),
                ('post_time', models.DateTimeField(auto_now_add=True)),
                ('refundable', models.BooleanField(default=False)),
                ('home_delivery', models.BooleanField(default=False)),
                ('slug', models.SlugField(unique=True)),
                ('category', models.ForeignKey(to='shop.Category')),
                ('owner', models.ForeignKey(to='shop.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SaleItemImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=b'sale_item_images', blank=True)),
                ('sale_item', models.ForeignKey(to='shop.SaleItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserBid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_time', models.DateTimeField(auto_now_add=True)),
                ('offer_price', models.IntegerField(default=0)),
                ('message', models.CharField(max_length=b'50')),
                ('sale_item', models.ForeignKey(to='shop.SaleItem')),
                ('user', models.ForeignKey(to='shop.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='post',
            name='poster',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='post',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.AddField(
            model_name='comment',
            name='sale_item',
            field=models.ForeignKey(default='', to='shop.SaleItem'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_last_edited',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_text',
            field=models.TextField(max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_time',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='seller_points',
            field=models.IntegerField(default=0, verbose_name=b'concrete measurement of reliability of this person as a seller'),
            preserve_default=True,
        ),
    ]
