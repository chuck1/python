from django.contrib import admin

# Register your models here.

from kitchen.models import MeasurementType
from kitchen.models import Unit
from kitchen.models import Item
from kitchen.models import Recipe
from kitchen.models import RecipeOrder
from kitchen.models import Ingredient
from kitchen.models import Transaction

import kitchen.models

admin.site.register(kitchen.models.MeasurementType)
admin.site.register(kitchen.models.Unit)
#admin.site.register(Item)
#admin.site.register(Recipe)
admin.site.register(kitchen.models.RecipeOrder)
admin.site.register(kitchen.models.Ingredient)
admin.site.register(kitchen.models.Transaction)
admin.site.register(kitchen.models.Category)
admin.site.register(kitchen.models.CategoryRelation)
#admin.site.register(kitchen.models.StoreCategory)



class IngredientInline(admin.TabularInline):
    model = kitchen.models.Ingredient
    extra = 1

class StoreCategoryInline(admin.TabularInline):
    model = kitchen.models.StoreCategory
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)

class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)

class StoreAdmin(admin.ModelAdmin):
    inlines = (StoreCategoryInline,)


admin.site.register(kitchen.models.Item,   ItemAdmin)
admin.site.register(kitchen.models.Recipe, RecipeAdmin)
admin.site.register(kitchen.models.Store,  StoreAdmin)



