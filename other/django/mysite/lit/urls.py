
from django.conf.urls import patterns, url

import lit.views

urlpatterns = patterns('',
    #url(r'transaction/$', views.TransactionList.as_view()),
    url(r'^$', lit.views.index, name='index'),
    url(r'^mybib.bib$', lit.views.bib, name='bib'),
    )


