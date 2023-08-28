from django import forms
from django.contrib.auth import get_user_model

from .models import Business, Property, Staff, StaffRoles

User = get_user_model()


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ("created_by",)


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ("is_active", "business")


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ("user", "role")

    def __init__(self, user, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        # user
        self.fields["user"].queryset = User.objects.exclude(pk=user.pk)
        self.fields["user"].empty_label = "Select a User . . . . "

        # Roles
        self.fields["role"].widget.choices = StaffRoles.choices

        # Add 'form-control' class to each field's widget
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({"class": "form-control"})
