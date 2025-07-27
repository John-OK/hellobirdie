from django.contrib import admin
from .models import Bird


class BirdAdmin(admin.ModelAdmin):
    list_display = ("english_name", "genus", "species", "subspecies")
    search_fields = ("genus", "species", "subspecies", "english_name")
    list_filter = ("genus", "species")
    empty_value_display = "—"


admin.site.register(Bird, BirdAdmin)
