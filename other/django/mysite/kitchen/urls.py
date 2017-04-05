from django.conf.urls import patterns, url

from kitchen import views

urlpatterns = patterns('kitchen.views',
    #url(r'transaction/$', views.TransactionList.as_view()),
    url(r'^$',                     views.index, name="index"),
    url(r'tree/$',                 views.tree,  name="tree"),
    url(r'item/$',                 views.ItemList.as_view()),
    url(r'inventory/$',            views.inventory,         name='inventory'),
    url(r'shoppinglist/$',         views.shoppinglist_view, name='shoppinglist'),
    url(r'add_recipe/$',           views.add_recipe,        name='add_recipe'),
    url(r'^(?P<recipe_id>\d+)/create_recipe_order/$',   views.create_recipe_order, name='create_recipe_order'),
    url(r'^(?P<recipe_id>\d+)/recipe_edit/$',           views.recipe_edit,         name='recipe_edit'),
    url(r'create_recipe/$',        views.create_recipe,    name='create_recipe'),
    url(r'recipeorder_list/$',     views.recipeorder_list, name='recipeorder_list'),
    url(r'recipe_list/$',          views.recipe_list,      name='recipe_list'),
    url(r'^(?P<recipeorder_id>\d+)/recipeorder_edit/$', views.recipeorder_edit,    name='recipeorder_edit'),
    url(r'ingredient_add',         views.ingredient_add,    name='ingredient_add'),
    url(r'ingredient_create',      views.ingredient_create, name='ingredient_create'),
    url(r'item_selector/$',        views.item_selector,       name='item_selector'),
    url(r'item_selector_final/$',  views.item_selector_final, name='item_selector_final'),
    url(r'item_selector_test/$',   views.item_selector_test, name='item_selector_test'),
    )

