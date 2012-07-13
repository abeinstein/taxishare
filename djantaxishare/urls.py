from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'taxis.views.home'),
    url(r'^taxis/', include('taxis.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
