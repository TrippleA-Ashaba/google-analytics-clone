from django.contrib import admin

from .models import Business, Property, Staff, Page, Event

# Register your models here.
admin.site.register(Business)
admin.site.register(Property)
admin.site.register(Staff)
admin.site.register(Event)
admin.site.register(Page)
