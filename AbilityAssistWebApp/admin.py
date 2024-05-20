from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Trip, FinalGeolocation, InitialGeolocation, AboutImage, LocationUpdate
import csv
from django.http import HttpResponse

# Define the export to CSV action
def export_to_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])
    return response

export_to_csv.short_description = "Export Selected to CSV"

# Extend the BaseUserAdmin class to include the export action
class UserAdmin(BaseUserAdmin):
    actions = [export_to_csv]

# ModelAdmin classes for your models
class TripAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_point', 'end_point', 'date', 'distance', 'duration') # Fields to display in list view
    actions = [export_to_csv]

class FinalGeolocationAdmin(admin.ModelAdmin):
    list_display = ('value', 'name')  # Fields to display in list view
    actions = [export_to_csv]

class InitialGeolocationAdmin(admin.ModelAdmin):
    list_display = ('longitude', 'latitude', 'updated_at')  # Fields to display in list view
    actions = [export_to_csv]

# Unregister the original UserAdmin and register the new UserAdmin with export action
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here
admin.site.register(Trip, TripAdmin)
admin.site.register(FinalGeolocation, FinalGeolocationAdmin)
admin.site.register(InitialGeolocation, InitialGeolocationAdmin)
admin.site.register(AboutImage)
admin.site.register(LocationUpdate)
