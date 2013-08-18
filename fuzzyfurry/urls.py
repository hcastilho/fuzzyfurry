from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^fuzzy/', include('fuzzyfurry.apps.fuzzy.urls')),
    # Examples:
    # url(r'^$', 'fuzzyfurry.views.home', name='home'),
    # url(r'^fuzzyfurry/', include('fuzzyfurry.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
