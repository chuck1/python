from django.contrib import admin

# Register your models here.

from lit.models import Publication
from lit.models import Author
from lit.models import Tag
from lit.models import Type

#admin.site.register(Publication)
admin.site.register(Author)
admin.site.register(Type)
#admin.site.register(Tag)

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('code','title')


class PublicationInline(admin.TabularInline):
    model = Publication.tags.through
    extra = 1

class TagAdmin(admin.ModelAdmin):
    inlines = (PublicationInline,)


admin.site.register(Publication, PublicationAdmin)
admin.site.register(Tag, TagAdmin)


