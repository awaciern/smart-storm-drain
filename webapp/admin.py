from django.contrib import admin
from .models import Device, Transmission, GatewayLog


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Device, DeviceAdmin)


class TransmissionAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'device', 'depth', 'flowrate', 'voltage']

admin.site.register(Transmission, TransmissionAdmin)


class GatewayLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'message', 'raw_data']

admin.site.register(GatewayLog, GatewayLogAdmin)
