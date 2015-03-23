from django.contrib.auth.models import User
from django.db import models
import itertools
from django.template.defaultfilters import slugify



class SellerProfile(models.Model):
	user = models.OneToOneField(User)
	location = models.CharField(max_length=30,blank=True)
	phone_number = models.IntegerField(default=1)


	def __unicode__(self):
		return (self.user.first_name + ' ' + self.user.last_name)

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
	current_highest_bid = models.IntegerField(default=0,blank=True)

	def save(self, *args, **kwargs):

		if not self.slug:
			self.slug = orig = slugify(self.title)
			for x in itertools.count(1):
				if not SaleItem.objects.filter(slug=self.slug).exists():
					break
				self.slug = '%s-%d' % (orig, x)
			super(SaleItem, self).save(*args, **kwargs)

		else:
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
	user = models.ForeignKey(User)
	sale_item = models.ForeignKey('SaleItem')
	post_time = models.DateTimeField(auto_now_add=True)
	offer_price = models.IntegerField(default=0)

	def __unicode__(self):
		return (self.user.first_name + " " + self.user.last_name + " " + self.sale_item.title)


class SaleItemImage(models.Model):
	image = models.ImageField(upload_to='sale_item_images',null=True,blank=True)
	sale_item = models.ForeignKey('SaleItem')

class Comment(models.Model):
	poster = models.ForeignKey('SellerProfile')
	sale_item = models.ForeignKey('SaleItem')
	comment_text = models.TextField(max_length=150)
	comment_time = 	models.DateTimeField(auto_now_add=True)
	comment_last_edited = models.DateTimeField(auto_now=True)
