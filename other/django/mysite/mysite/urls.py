from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^kitchen/',  include('kitchen.urls',  namespace="kitchen")),
    url(r'^lit/',   include('lit.urls',   namespace="lit")),
    url(r'^wiki/',  include('wiki.urls',  namespace="wiki")),
    url(r'^climb/', include('climb.urls', namespace="climb")),
    url(r'^admin/', include(admin.site.urls)),
)

