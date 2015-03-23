from django import forms
from shop.models import SaleItem, Category, UserBid, SellerProfile

class SaleItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    class Meta:
        model = SaleItem
        fields = ('title','condition','description','reason',
                  'asking_price','negotiable','category',)

class UserBidForm(forms.ModelForm):
    class Meta:
        model = UserBid
        fields = ('offer_price',)

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ('seller_name','location',
                  'phone_number','payment_type',
                  'home_delivery','meetup',
	              'details',)