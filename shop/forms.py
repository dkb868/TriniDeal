from django import forms
from shop.models import SaleItem, Category, UserBid, SellerProfile, Order


class SaleItemForm(forms.ModelForm):
	category = forms.ModelChoiceField(queryset=Category.objects.all())
	image = forms.ImageField(required=True)
	additional_images = forms.ImageField(required=False)
	class Meta:
		model = SaleItem
		fields = ('title','condition','description','reason',
				  'asking_price','negotiable','category','image','additional_images')

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
				  'details','image')

	def clean(self):
		cleaned_data = super(SellerProfileForm, self).clean()
		meetup = cleaned_data.get('meetup')
		home_delivery = cleaned_data.get('home_delivery')

		if not (meetup or (home_delivery!='NONE')):
			raise forms.ValidationError({'meetup': ['You need some way to deliver your products...',]})

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
			raise forms.ValidationError({'meetuploc': ['You need to enter the details for some method of delivery',]})
class OrderConfirmationForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('agreetoterms',)

	def clean(self):
		cleaned_data = super(OrderConfirmationForm, self).clean()
		agree = cleaned_data.get('agreetoterms')

		if not agree:
			raise forms.ValidationError({'agreetoterms': ['You must agree to the terms to continue',]})

class SignupForm(forms.Form):
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)

	def signup(self, request, user):
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.save()


## dummy item hack

class DummyItemForm(forms.ModelForm):
	category = forms.ModelChoiceField(queryset=Category.objects.all())
	image = forms.ImageField(required=True)
	additional_images = forms.ImageField(required=False)
	class Meta:
		model = SaleItem
		fields = ('title','condition','description','reason',
				  'asking_price','negotiable','category','image','additional_images','dummyseller','dummydelivery','dummylocation','dummynumber' )