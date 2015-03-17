from django.contrib import admin
from shop.models import UserProfile,Comment, Post
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Post)

