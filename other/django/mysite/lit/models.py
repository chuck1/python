from django.db import models

# Create your models here.

from django.contrib import admin

class Author(models.Model):
    name1 = models.CharField(max_length=128)
    name2 = models.CharField(max_length=128)
    
    def __unicode__(self):
        return self.name1 + ", " + self.name2

class Type(models.Model):
    name = models.CharField(max_length=64)
    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=64)
    def __unicode__(self):
        return self.name

class Publication(models.Model):
    title = models.CharField(max_length=512)
    _type = models.ForeignKey(Type, null=True)
    bib = models.TextField()
    authors = models.ManyToManyField(Author, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    code = models.CharField(max_length=128, null=True, default="")
    
    def __unicode__(self):
        return str(self.code) + ":" + self.title


