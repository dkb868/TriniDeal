from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings


urlpatterns = patterns('',
    url(r'^$', 'shop.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^review/', include('review.urls')),
    #namespace everything
    url(r'^shop/', include('shop.urls', namespace='shop')),
)

#development media server
if settings.DEBUG:
        urlpatterns += patterns(
            'django.views.static',
            (r'^media/(?P<path>.*)',
            'serve',
            {'document_root': settings.MEDIA_ROOT}),
        )