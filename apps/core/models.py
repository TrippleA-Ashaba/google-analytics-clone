from django.db import models
from apps.accounts.models import CustomUser


# Create your models here.
class Business(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    business_sector = models.CharField(max_length=50, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    business = models.ManyToManyField(Business, related_name="business")
    created_at = models.DateTimeField(auto_now_add=True)
