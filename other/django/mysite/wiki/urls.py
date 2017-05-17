
from django.conf.urls import patterns, url

import wiki.views

urlpatterns = patterns('',
    #url(r'transaction/$', views.TransactionList.as_view()),
    url(r'^$', wiki.views.index, name='index'),
    url(r'^page/(?P<page>[\w\/]+).html$', wiki.views.page, name='page'),
    )



