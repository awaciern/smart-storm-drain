from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    fields = ['text', 'date']

admin.site.register(Message, MessageAdmin)
