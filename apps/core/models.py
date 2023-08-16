from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Business(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    business_sector = models.CharField(max_length=50, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Property(models.Model):
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        help_text="Add a business first in None is registered",
    )
    name = models.CharField("Property Name", max_length=100, blank=False, null=False)
    domain = models.URLField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Properties"

    def __str__(self) -> str:
        return self.name


class StaffRoles(models.TextChoices):
    VIEWER = "viewer", "Viewer"
    EDITOR = "editor", "Editor"


class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(
        Property, related_name="staff", on_delete=models.CASCADE
    )
    role = models.CharField(max_length=50, choices=StaffRoles.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "property")

    def __str__(self) -> str:
        return self.user.get_full_name()
