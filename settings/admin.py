from django.contrib import admin
from .models import Vehicle_Setting

class VehicleSettingAdmin(admin.ModelAdmin):
    list_display = ('login', 'type', 'info', 'booked',)
    search_fields = ('login', 'type',)

admin.site.register(Vehicle_Setting, VehicleSettingAdmin)
