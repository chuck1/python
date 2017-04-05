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

#class CategoryBase(models.Model):
#    class Meta:
#        #abstract = True
#        pass

#class CategoryRelation(models.Model):
#    parent = models.ForeignKey(CategoryBase,related_name='+')
#    child  = models.ForeignKey(CategoryBase,related_name='+')

#class Category(CategoryBase):
class Category(models.Model):
    name   = models.CharField(max_length=256)
    #parent = models.ForeignKey(Category, null=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class CategoryRelation(models.Model):
    parent = models.ForeignKey(Category,related_name='+')
    child  = models.ForeignKey(Category,related_name='+')

    def __unicode__(self):
        return self.parent.name + " --- " + self.child.name
   

class Item(models.Model):

    name = models.CharField(max_length=256)
    unit = models.ForeignKey(Unit, null=True)

    category = models.ForeignKey(Category, null=True)
    price  = models.FloatField(null=True)

    def __unicode__(self):
        #return "Item:" + self.name
        return self.name

    def get_category(self):
        
        c = self.category

        while True:
            lst_cr = CategoryRelation.objects.filter(child = c)
            
            if not lst_cr:
                return c
            else:
                c = lst_cr[0].parent

    class Meta:
        ordering = ('name',)

class Recipe(models.Model):
    name = models.CharField(max_length=256)
    source = models.CharField(max_length=256, blank=True)
    lcm = models.FloatField(default=1.0)
    ingredients = models.ManyToManyField(Item, through='Ingredient')
    text = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return "Recipe:" + self.name
    def can_make(self, a, ir_dict):
        #print("can_make")
        #print(ir_dict)

        ings = Ingredient.objects.filter(recipe=self, amount__gt=0)
        
        #print(ings)

        for ing in ings:
            need = a * ing.amount_std

            if not ing.item in ir_dict:
                if need > 0:
                    return False

            ir = ir_dict[ing.item]
            
            if ir < need:
                return False

        return True

class RecipeOrder(models.Model):

    PLANNED  = '0'
    COMPLETE = '1'
    CANCELED = '2'
    STATUS_CHOICES = (
        (PLANNED,  'planned'),
        (COMPLETE, 'complete'),
        (CANCELED, 'canceled'),
        )
                        
    recipe = models.ForeignKey(Recipe)
    amount = models.FloatField()
    status = models.CharField(max_length=1,
        choices=STATUS_CHOICES,
        default=PLANNED)

    def __unicode__(self):
        return self.recipe.name + ": " + str(self.amount)

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    item = models.ForeignKey(Item)
    unit = models.ForeignKey(Unit)
    amount = models.FloatField()
    optional = models.BooleanField(default=False)
    def __unicode__(self):
        return self.recipe.name + ": " + self.item.name
    def _get_amount_std(self):
        return self.amount * self.unit.convert
    amount_std = property(_get_amount_std)
    
class RecipeOrderTransaction(models.Model):
    recipeorder = models.ForeignKey(RecipeOrder)
    ingredient  = models.ForeignKey(Ingredient)
    unit        = models.ForeignKey(Unit)
    amount      = models.FloatField()

    def _get_amount_std(self):
        return self.amount * self.unit.convert

    amount_std = property(_get_amount_std)

class Transaction(models.Model):
    item   = models.ForeignKey(Item)
    unit   = models.ForeignKey(Unit)
    amount = models.FloatField()
    def __unicode__(self):
        return self.item.name + ":" + str(self.amount_std)
    def _get_amount_std(self):
        return self.amount * self.unit.convert
    amount_std = property(_get_amount_std)

class Store(models.Model):
    name = models.CharField(max_length=256)
    categories = models.ManyToManyField(Category, through='StoreCategory')
 
    def __unicode__(self):
        return self.name
   
class StoreCategory(models.Model):
    store    = models.ForeignKey(Store)
    category = models.ForeignKey(Category)
    order    = models.FloatField()

    class Meta:
        ordering = ('order',)
    












