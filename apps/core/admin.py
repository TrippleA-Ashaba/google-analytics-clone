from django.contrib import admin

from .models import Business, Property, Staff

# Register your models here.
admin.site.register(Business)
admin.site.register(Property)
admin.site.register(Staff)
