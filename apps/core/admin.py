from django.contrib import admin

from .models import Business, Staff, Property

# Register your models here.
admin.site.register(Business)
admin.site.register(Property)
admin.site.register(Staff)
