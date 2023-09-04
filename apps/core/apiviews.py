from django.db import IntegrityError
from rest_framework import generics

from .models import Property
from .serializers import UserActivitySerializer


class UserActivityApiView(generics.CreateAPIView):
    serializer_class = UserActivitySerializer

    def perform_create(self, serializer, *args, **kwargs):
        token = self.kwargs.get("web_token", None)
        print(token, "*" * 50)
        website = Property.objects.get(token=token)
        print(website, "*" * 50)

        user_agent = serializer.validated_data["user_agent"]
        print(user_agent)
        try:
            serializer.save(user_agent=user_agent, website=website)
        except IntegrityError:
            pass
