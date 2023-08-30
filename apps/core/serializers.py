from rest_framework import serializers

from .models import SitePost


class SitePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SitePost
        fields = "__all__"
