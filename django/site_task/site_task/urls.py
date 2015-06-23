from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'site_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^task/',  include('task.urls',  namespace='task')),
    url(r'^admin/', include(admin.site.urls)),
)
