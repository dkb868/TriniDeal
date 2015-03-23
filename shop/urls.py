from django.conf.urls import patterns, url, include
from shop import views

urlpatterns = patterns('',
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^item/(?P<item_slug>[\w\-]+)/$', views.saleitem, name='item'),
    url(r'^add_new_item/$', views.add_new_item, name='add_new_item'),
    url(r'^sellerprofile/(?P<user_id>\d+)/$', views.sellerprofile, name='sellerprofile'),
    url(r'^dashboard/$', views.sellerdashboard, name='dashboard'),
    url(r'^make_bid/(?P<item_slug>[\w\-]+)/$', views.make_bid, name='makebid'),
    url(r'^create_sellerprofile/$', views.create_sellerprofile, name='create_sellerprofile'),
	)
