from django import forms

from .models import Business, Staff, Property


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ("created_by",)


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ("is_active",)

    def __init__(self, user, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.fields["business"].queryset = Business.objects.filter(created_by=user)


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = "__all__"
