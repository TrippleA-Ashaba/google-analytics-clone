from rest_framework import generics
from user_agents import parse
from .models import Property
from django.db import IntegrityError
from .serializers import UserActivitySerializer


class UserActivityApiView(generics.CreateAPIView):
    serializer_class = UserActivitySerializer

    def perform_create(self, serializer, *args, **kwargs):
        token = self.kwargs.get("token", None)
        website = Property.objects.get(token=token)

        user_agent_string = serializer.validated_data["user_agent"]
        user_agent = parse(user_agent_string)
        try:
            serializer.save(user_agent=user_agent, website=website)
        except IntegrityError:
            pass
