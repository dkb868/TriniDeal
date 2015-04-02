from django import template
from shop.models import Category, SaleItem
from django.template import RequestContext

register = template.Library()

@register.inclusion_tag('shop/cats.html')
def get_category_list(cat=None):
	return {'cats': Category.objects.all(), 'act_cat': cat}

@register.assignment_tag
def get_cats():
	return Category.objects.all()

@register.assignment_tag
def get_item_condition(item_slug):
	item = SaleItem.objects.get(slug=item_slug)
	condition = item.get_condition_display()
	return condition