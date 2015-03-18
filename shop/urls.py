from django.conf.urls import patterns, url
from shop import views

urlpatterns = patterns('',
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^item/(?P<item_slug>[\w\-]+)/$', views.saleitem, name='item'),

    # Social User set up required for the following views to work
#    url(r'^sellerprofile/(?P<user_id>\d+)/$', views.sellerprofile, name='sellerprofile'),
#    url(r'^dashboard/$', views.sellerdashboard, name='dashboard'),
	)
