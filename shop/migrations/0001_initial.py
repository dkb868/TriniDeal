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
                ('parent_category', models.ForeignKey(blank=True, to='shop.Category', null=True)),
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
                ('poster', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meetuploc', models.TextField(blank=True)),
                ('street', models.TextField(blank=True)),
                ('city', models.TextField(blank=True)),
                ('phone', models.IntegerField()),
                ('additionalinfo', models.TextField(blank=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('agreetoterms', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50)),
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
                ('description', models.TextField(blank=True)),
                ('asking_price', models.IntegerField(default=0)),
                ('negotiable', models.BooleanField(default=True)),
                ('available', models.BooleanField(default=True)),
                ('post_time', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True)),
                ('reason', models.CharField(max_length=100, blank=True)),
                ('image', models.ImageField(upload_to=b'sale_item_images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SaleItemAdditionalImages',
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
                ('seller_name', models.CharField(max_length=50, blank=True)),
                ('location', models.CharField(max_length=30, blank=True)),
                ('phone_number', models.IntegerField(default=1)),
                ('home_delivery', models.CharField(max_length=5, choices=[(b'SOME', b'Some Locations'), (b'ALL', b'All locations'), (b'NONE', b'No home delivery')])),
                ('meetup', models.BooleanField(default=True)),
                ('details', models.TextField(blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'sellerprofile_images', blank=True)),
                ('payment_type', models.ManyToManyField(to='shop.PaymentChoice')),
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
                ('sale_item', models.ForeignKey(to='shop.SaleItem')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='accepted_bid',
            field=models.OneToOneField(null=True, blank=True, to='shop.UserBid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='saleitem',
            name='category',
            field=models.ForeignKey(to='shop.Category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='saleitem',
            name='owner',
            field=models.ForeignKey(to='shop.SellerProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='buy_item',
            field=models.OneToOneField(to='shop.SaleItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='buyer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='paymentmethod',
            field=models.ForeignKey(to='shop.PaymentChoice'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='sale_item',
            field=models.ForeignKey(to='shop.SaleItem'),
            preserve_default=True,
        ),
    ]
