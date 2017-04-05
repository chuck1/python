from django.db import models

# Create your models here.

class Location(models.Model):
    name     = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

class Area(models.Model):
    name     = models.CharField(max_length=256)
    location = models.ForeignKey(Location)
    
    def __unicode__(self):
        return self.name

class Wall(models.Model):
    name     = models.CharField(max_length=256)
    area     = models.ForeignKey(Area)
    
    def __unicode__(self):
        return self.name

class Route(models.Model):
    name     = models.CharField(max_length=256)
    wall     = models.ForeignKey(Wall)
    
    def __unicode__(self):
        return self.name

class Pitch(models.Model):
    name     = models.CharField(max_length=256)
    route    = models.ForeignKey(Route)

    def __unicode__(self):
        return self.name

class Climb(models.Model):
    date     = models.DateField()
    pitch    = models.ForeignKey(Pitch)





