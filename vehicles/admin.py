from django.contrib import admin

from .models import Vehicle_Fuel, Vehicle_Fuel_Pos, Vehicle_Type


class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('login', 'type', 'aktiv', 'label')


class VehicleFuelAdmin(admin.ModelAdmin):
    list_display = ('login', 'type', 'info', 'booked',)
    search_fields = ('login', 'type',)

class VehicleFuelPosAdmin(admin.ModelAdmin):
    list_display = ('fuel_id', 'pos', 'amount', 'km', 'liter', 'booked')

admin.site.register(Vehicle_Type, VehicleTypeAdmin)
admin.site.register(Vehicle_Fuel, VehicleFuelAdmin)
admin.site.register(Vehicle_Fuel_Pos, VehicleFuelPosAdmin)
