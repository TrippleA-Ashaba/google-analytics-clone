from django import forms

from .models import Business, Staff


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ("is_active",)


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = "__all__"
