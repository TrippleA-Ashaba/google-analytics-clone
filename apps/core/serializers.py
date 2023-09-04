from rest_framework import serializers

from .models import UserActivity


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        exclude = ("website",)
