from django.db import models

# Create your models here.

class MeasurementType(models.Model):
    name = models.CharField(max_length=256)
    def __unicode__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=256)
    measurementtype = models.ForeignKey(MeasurementType)
    
    convert = models.FloatField(null=True)
    
    def __unicode__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=256)
    def __unicode__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=256)
    def __unicode__(self):
        return self.name

class RecipeOrder(models.Model):
    recipe = models.ForeignKey(Recipe)
    amount = models.FloatField()

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    item = models.ForeignKey(Item)
    unit = models.ForeignKey(Unit)
    amount = models.FloatField()
    def __unicode__(self):
        return self.recipe.name
    def _get_amount_std(self):
        return self.amount * self.unit.convert
    amount_std = property(_get_amount_std)

class Transaction(models.Model):
    item = models.ForeignKey(Item)
    unit = models.ForeignKey(Unit)
    amount = models.FloatField()
   
    def _get_amount_std(self):
        return self.amount * self.unit.convert
    amount_std = property(_get_amount_std)

