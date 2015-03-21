from django import forms
from shop.models import SaleItem, Category, UserBid


class SaleItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    class Meta:
        model = SaleItem
        fields = ('title','condition','description',
                  'asking_price','payment_type','negotiable',
                  'expiration_date', 'category','refundable',
                  'home_delivery',)

class UserBidForm(forms.ModelForm):
    class Meta:
        model = UserBid
        fields = ('offer_price',)