from django.db import models

# Create your models here.

#UserProfile not user. Email,password etc is already done by django.
#Social login will be used
#Thus userProfile only needs additional info like rating etc.

class UserProfile(models.Model):

	seller_points = models.IntegerField(verbose_name='concrete measurement of reliability of this person as a seller')
	#seller points may be earned by being upvoted by satisfied customers, commenting a lot, etc.
	#no password field as I would encourage the use of Facebook/other oauth2 login in lieu of inconvenient accounts
	
class Post(models.Model):
	
	post_type_choices = (('buy','Buying'), ('sell','Selling'))
	
	post_type = models.CharField(max_length = 4, choices = post_type_choices, default='sell')
	poster = models.ForeignKey('UserProfile')
	post_text = models.TextField(max_length=1500)
	sale_category = models.CharField(max_length=75)
	post_time = models.DateTimeField()
	post_last_edited = models.DateTimeField()
	price = models.IntegerField()
	availability = models.BooleanField(default=True)
	
	
class Comment(models.Model):
	poster = models.ForeignKey('UserProfile')
	post = models.ForeignKey('Post')
	comment_text = models.TextField(max_length=1500)
	comment_time = 	models.DateTimeField()	
	comment_last_edited = models.DateField()
