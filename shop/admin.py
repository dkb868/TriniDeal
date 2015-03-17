from django.contrib import admin
from shop.models import UserProfile, SaleItem, Category, UserBid, SaleItemImage, Comment

admin.site.register(UserProfile)
admin.site.register(SaleItem)
admin.site.register(Category)
admin.site.register(UserBid)
admin.site.register(SaleItemImage)
admin.site.register(Comment)

