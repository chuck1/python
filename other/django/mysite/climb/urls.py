from django.conf.urls import patterns, url

from climb import views

urlpatterns = patterns('climb.views',
    url(r'^$',                    views.index,           name="index"),
    url(r'location_list/$',       views.location_list,   name='location_list'),
    url(r'area_list/$',           views.area_list,       name='area_list'),
    url(r'wall_list/$',           views.wall_list,       name='wall_list'),
    url(r'route_list/$',          views.route_list,      name='route_list'),
    url(r'route_create/$',        views.route_create,    name='route_create'),
    url(r'pitch_list/$',          views.pitch_list,      name='pitch_list'),
    url(r'climb_create/$',        views.climb_create,    name='climb_create'),
    )



