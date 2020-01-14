from django.contrib import admin
from .models import Device, Transmission


# class MessageAdmin(admin.ModelAdmin):
#     fields = ['text', 'date']
#
# admin.site.register(Message, MessageAdmin)


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Device, DeviceAdmin)


class TransmissionAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'device', 'depth', 'flowrate']

admin.site.register(Transmission, TransmissionAdmin)
