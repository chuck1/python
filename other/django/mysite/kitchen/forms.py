import django.forms

import kitchen.models

class add_recipe(django.forms.Form):
    name   = django.forms.CharField(max_length=256)
    source = django.forms.CharField(max_length=256)
    lcm    = django.forms.FloatField()
    #ingredients = models.ManyToManyField(Item, through='Ingredient')
    #text   = django.forms.TextField()

class ingredient_add(django.forms.Form):
    unit   = django.forms.ModelChoiceField(queryset=kitchen.models.Unit.objects.all())
    amount = django.forms.DecimalField()

