from django import forms
from django.contrib.auth import get_user_model

from .models import Business, Property, Staff

User = get_user_model()


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

    def __init__(self, user, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields["property"].queryset = Property.objects.filter(
            business__created_by=user
        )
        self.fields["user"].queryset = User.objects.exclude(pk=user.pk)
