from django.contrib import admin
from train.models import Train, Station, Route
# Register your models here.


class trainAdmin(admin.ModelAdmin):
	list_display = ["number", "name"]

admin.site.register(Train)
admin.site.register(Station)
admin.site.register(Route)
