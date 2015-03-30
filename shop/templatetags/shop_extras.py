from django import template
from shop.models import Category
from django.template import RequestContext

register = template.Library()

@register.inclusion_tag('shop/cats.html')
def get_category_list(cat=None):
	return {'cats': Category.objects.all(), 'act_cat': cat}

@register.assignment_tag
def get_cats():
	return Category.objects.all()
