from django.conf.urls import patterns, url, include
from shop import views

urlpatterns = patterns('',
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^item/(?P<item_slug>[\w\-]+)/$', views.saleitem, name='item'),
    url(r'^add_new_item/$', views.add_new_item, name='add_new_item'),
    url(r'^sellerprofile/(?P<seller_id>\d+)/$', views.sellerprofile, name='sellerprofile'),
    url(r'^make_bid/(?P<item_slug>[\w\-]+)/$', views.make_bid, name='makebid'),
    url(r'^create_sellerprofile/$', views.create_sellerprofile, name='create_sellerprofile'),
    url(r'^(?P<item_slug>[\w\-]+)/shoppingcart/$', views.item_cart, name='item_cart'),
    url(r'^(?P<item_slug>[\w\-]+)/checkout/$', views.checkout, name='checkout'),
    url(r'^(?P<item_slug>[\w\-]+)/bidcheckout/$', views.bidcheckout, name='bidcheckout'),
    url(r'^confirmation/(?P<order_id>\d+)/$', views.confirmation, name='confirmation'),
    url(r'^acceptbid/(?P<bid_id>\d+)/$', views.acceptbid, name='acceptbid'),
    url(r'^order/(?P<order_id>\d+)/$', views.order, name='order'),
    url(r'^myorders/$', views.myorders, name='myorders'),


    # dashboard urls
    url(r'^dashboard/$', views.sellerdashboard, name='dashboard'),
    url(r'^dashboard/current_items/$', views.dashboard_current_items, name='dashboard_current_items'),
    url(r'^dashboard/past_items/$', views.dashboard_past_items, name='dashboard_past_items'),
    url(r'^dashboard/current_orders/$', views.dashboard_current_orders, name='dashboard_current_orders'),
    url(r'^dashboard/past_orders/$', views.dashboard_past_orders, name='dashboard_past_orders'),
    url(r'^(?P<item_slug>[\w\-]+)/remove_item/$', views.removeitem, name='removeitem'),
    url(r'^(?P<item_slug>[\w\-]+)/reactivate_item/$', views.reactivateitem, name='reactivateitem'),

	)
