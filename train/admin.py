from django.contrib import admin
from train.models import Train, Station, Route, Review, Location
# Register your models here.


class trainAdmin(admin.ModelAdmin):
	list_display = ["number", "name"]

admin.site.register(Train)
admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Review)
admin.site.register(Location)
