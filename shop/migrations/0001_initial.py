# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=b'20')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_text', models.TextField(max_length=150)),
                ('comment_time', models.DateTimeField(auto_now_add=True)),
                ('comment_last_edited', models.DateTimeField(auto_now=True)),
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
                ('condition', models.CharField(max_length=15, choices=[(b'NEW', b'New'), (b'LIKENEW', b'Like New/Barely Used'), (b'REFURBISHED', b'Refurbished'), (b'USEDVERYGOOD', b'Used - Very Good'), (b'USEDGOOD', b'Used - Good'), (b'USEDACCEPTABLE', b'Used - Acceptable')])),
                ('description', models.TextField(max_length=b'200', blank=True)),
                ('asking_price', models.IntegerField(default=0)),
                ('payment_type', models.CharField(max_length=6, choices=[(b'COD', b'Cash On Delivery'), (b'ONLINE', b'Paypal')])),
                ('negotiable', models.BooleanField(default=True)),
                ('expiration_date', models.DateField(null=True, blank=True)),
                ('available', models.BooleanField(default=True)),
                ('post_time', models.DateTimeField(auto_now_add=True)),
                ('refundable', models.BooleanField(default=False)),
                ('home_delivery', models.BooleanField(default=False)),
                ('slug', models.SlugField(unique=True)),
                ('category', models.ForeignKey(to='shop.Category')),
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
            name='SellerProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
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
                ('message', models.CharField(max_length=b'50', blank=True)),
                ('sale_item', models.ForeignKey(to='shop.SaleItem')),
                ('user', models.ForeignKey(to='shop.SellerProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='owner',
            field=models.ForeignKey(to='shop.SellerProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='poster',
            field=models.ForeignKey(to='shop.SellerProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='sale_item',
            field=models.ForeignKey(to='shop.SaleItem'),
            preserve_default=True,
        ),
    ]
