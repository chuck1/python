from django.contrib import admin

# Register your models here.

import climb.models

admin.site.register(climb.models.Location)
admin.site.register(climb.models.Area)
admin.site.register(climb.models.Wall)
admin.site.register(climb.models.Route)

