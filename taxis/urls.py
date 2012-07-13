from django.conf.urls import patterns, include, url

urlpatterns = patterns('taxis.views',
    url(r'^$', 'index'),
    url(r'^(?P<taxi_id>\d+)/$', 'detail'),
    url(r'^addTaxi/$', 'addTaxi'),
)