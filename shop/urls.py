from django.conf.urls import patterns, url, include

from shop import views

urlpatterns = patterns('',
	url(r'^$', views.example, name='example'),
	)
	
