from django.contrib.auth.models import User
from django.db import models
import itertools
from django.template.defaultfilters import slugify

class PaymentChoice(models.Model):
	description = models.CharField(max_length=50)

	def __unicode__(self):
		return self.description

class SellerProfile(models.Model):

	# Choice Lists
	DELIVERY_CHOICES = (
		('SOME', 'Some Locations'),
		('ALL', 'All locations'),
		('NONE', 'No home delivery'),
	)

	# Model Fields
	user = models.OneToOneField(User)
	seller_name = models.CharField(max_length=50,blank=True)
	location = models.CharField(max_length=30,blank=True)
	phone_number = models.IntegerField(default=1)
	payment_type = models.ManyToManyField('PaymentChoice')
	home_delivery = models.CharField(max_length=5, choices=DELIVERY_CHOICES)
	meetup = models.BooleanField(default=True)
	details = models.TextField(blank=True)



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



	# Model Fields

	owner = models.ForeignKey('SellerProfile')
	title = models.CharField(max_length='30')
	condition = models.CharField(max_length=15, choices=CONDITION_CHOICES)
	description = models.TextField(blank=True)
	asking_price = models.IntegerField(default=0)
	negotiable = models.BooleanField(default=True)
	available = models.BooleanField(default=True, blank=True)
	post_time = models.DateTimeField(auto_now_add=True)
	category = models.ForeignKey('Category')
	slug = models.SlugField(unique=True)
	reason = models.CharField(max_length=100, blank=True)
	accepted_bid = models.OneToOneField('UserBid', null=True, blank=True)

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
	poster = models.ForeignKey(User)
	sale_item = models.ForeignKey('SaleItem')
	comment_text = models.TextField(max_length=150)
	comment_time = 	models.DateTimeField(auto_now_add=True)

class Order(models.Model):

	PAYMENT_CHOICES = (
		('COD', 'Cash on delivery'),
		('CARD', 'Linx/Debit Card/Credit Card on delivery'),
		('ONLINE', ''),
	)
	buyer = models.ForeignKey(User)
	buy_item = models.OneToOneField('SaleItem')
	meetuploc = models.TextField(blank=True)
	street = models.TextField(blank=True)
	city = models.TextField(blank=True)
	phone = models.IntegerField()
	paymentmethod = models.CharField(max_length=7,choices=PAYMENT_CHOICES)
	additionalinfo = models.TextField(blank=True)
	confirmed = models.BooleanField(default=False)
	agreetoterms = models.BooleanField(default=False)
	completed = models.BooleanField(default=False)

	def __unicode__(self):
		return ("ORDER" + " " + self.buyer.first_name + " " + self.buyer.last_name + " " + self.buy_item.title )







