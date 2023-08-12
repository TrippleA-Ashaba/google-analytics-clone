from django import forms

from .models import Business, Staff


class BusinessForm(forms.ModelForm):
    class Meta:
        # db_table='business'
        model = Business
        exclude = ("is_active",)


class StaffForm(forms.ModelForm):
    class Meta:
        # db_table='staff'
        model = Staff
        fields = "__all__"
