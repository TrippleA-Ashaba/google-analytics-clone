from rest_framework import generics
from .serializers import SitePostSerializer

from .models import SitePost


class SitePostApiView(generics.CreateAPIView):
    serializer_class = SitePostSerializer
