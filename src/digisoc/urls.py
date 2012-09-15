from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/', include( 'digisoc.api.urls' ) ),
    url(r'^$', 'digisoc.frontend.views.index'),
)
