from django.db import models

# Create your models here.

class User(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField()
	#no password field as I would encourage the use of Facebook login in lieu of inconvenient accounts
	
class Post(models.Model):
	
	post_type_choices = (('buy','Buying'), ('sell','Selling'))
	
	post_type = models.CharField(max_length = 4, choices = post_type_choices, default='sell')
	poster = models.ForeignKey('User')
	post_text = models.TextField(max_length=1500)
	sale_category = models.CharField(max_length=75)
	post_time = models.DateField()
	post_last_edited = models.DateField()
	price = models.IntegerField()
	availability = models.BooleanField(default=True)
	
	
class Comment(models.Model):
	poster = models.ForeignKey('User')
	post = models.ForeignKey('Post')
	comment_text = models.TextField(max_length=1500)
	comment_time = 	models.DateField()	
	comment_last_edited = models.DateField()
	
