import django_filters
from shop.models import SaleItem

__author__ = 'mitrikyle'

class SaleItemFilter(django_filters.FilterSet):
	asking_price = django_filters.NumberFilter(lookup_type='lt')
	class Meta:
		model = SaleItem
		fields = ['asking_price']
		order_by = ['asking_price']