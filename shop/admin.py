from django.contrib import admin
from shop.models import SellerProfile, SaleItem, Category, UserBid, Comment, PaymentChoice, Order, SaleItemAdditionalImages

admin.site.register(SellerProfile)
admin.site.register(SaleItem)
admin.site.register(Category)
admin.site.register(UserBid)
admin.site.register(Comment)
admin.site.register(PaymentChoice)
admin.site.register(Order)
admin.site.register(SaleItemAdditionalImages)


