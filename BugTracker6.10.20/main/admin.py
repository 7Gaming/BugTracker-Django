from django.contrib import admin
from .models import Bug

class DisplayBug(admin.ModelAdmin):
    list_display = ('name', 'status', 'open_time', 'closed_time')

admin.site.register(Bug, DisplayBug)