from django.db import models
import itertools
from django.template.defaultfilters import slugify


# UserProfile not user. Email,password etc is already done by django.
# Social login will be used
# Thus userProfile only needs additional info like rating etc.
class SellerProfile(models.Model):

	seller_points = models.IntegerField(default=0,verbose_name='concrete measurement of reliability of this person as a seller')
	# seller points may be earned by being upvoted by satisfied customers, commenting a lot, etc.
	# no password field as I would encourage the use of Facebook/other oauth2 login in lieu of inconvenient accounts

class SaleItem(models.Model):

	# Choice Lists

	CONDITION_CHOICES = (
		('NEW', 'New'),
		('LIKENEW', 'Like New/Barely Used'),
		('REFURBISHED', 'Refurbished'),
		('USEDVERYGOOD', 'Used - Very Good'),
		('USEDGOOD', 'Used - Good'),
		('USEDACCEPTABLE', 'Used - Acceptable'),

	)

	PAYMENT_CHOICES = (
		('COD', 'Cash On Delivery'),
		('ONLINE', 'Paypal'),
	)

	# Model Fields

	owner = models.ForeignKey('SellerProfile')
	title = models.CharField(max_length='30')
	condition = models.CharField(max_length=15, choices=CONDITION_CHOICES)
	description = models.TextField(max_length='200',blank=True)
	asking_price = models.IntegerField(default=0)
	payment_type = models.CharField(max_length=6, choices=PAYMENT_CHOICES)
	negotiable = models.BooleanField(default=True)
	expiration_date = models.DateField(blank=True,null=True)
	available = models.BooleanField(default=True, blank=True)
	post_time = models.DateTimeField(auto_now_add=True)
	category = models.ForeignKey('Category')
	refundable = models.BooleanField(default=False)
	home_delivery = models.BooleanField(default=False)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):

		#if slug is already used, add a number to it.

		self.slug = orig = slugify(self.title)
		for x in itertools.count(1):
			if not SaleItem.objects.filter(slug=self.slug).exists():
				break
			self.slug = '%s-%d' % (orig, x)

		super(SaleItem, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.title

class Category(models.Model):
	name = models.CharField(max_length='20',unique=True)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)

		super(Category, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name



class UserBid(models.Model):
	user = models.ForeignKey('SellerProfile')
	sale_item = models.ForeignKey('SaleItem')
	post_time = models.DateTimeField(auto_now_add=True)
	offer_price = models.IntegerField(default=0)
	# user bids may optionally have short messages with them.
	message = models.CharField(max_length='50', blank=True)


class SaleItemImage(models.Model):
	image = models.ImageField(upload_to='sale_item_images',null=True,blank=True)
	sale_item = models.ForeignKey('SaleItem')

class Comment(models.Model):
	poster = models.ForeignKey('SellerProfile')
	sale_item = models.ForeignKey('SaleItem')
	comment_text = models.TextField(max_length=150)
	comment_time = 	models.DateTimeField(auto_now_add=True)
	comment_last_edited = models.DateTimeField(auto_now=True)
