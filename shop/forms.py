from django import forms
from shop.models import SaleItem, Category, UserBid, SellerProfile, Order


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

class OrderCheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('meetuploc','street',
                  'city','phone',
                  'paymentmethod', 'additionalinfo',)

    def clean(self):
        cleaned_data = super(OrderCheckoutForm, self).clean()
        meetuploc = cleaned_data.get('meetuploc')
        street = cleaned_data.get('street')
        city = cleaned_data.get('city')

        if not (meetuploc or (street and city)):
            raise forms.ValidationError('You need to enter the details for some method of delivery')

class OrderConfirmationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('agreetoterms',)

    def clean(self):
        cleaned_data = super(OrderConfirmationForm, self).clean()
        agree = cleaned_data.get('agreetoterms')

        if not agree:
            raise forms.ValidationError('You must agree to the terms to continue')
