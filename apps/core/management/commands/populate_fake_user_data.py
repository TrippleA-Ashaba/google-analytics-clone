# Populate fake user activity


import random

from django.core.management.base import BaseCommand
from faker import Faker

from apps.core.models import Event, Page, Property, UserActivity


class Command(BaseCommand):
    help = "Populates the database with fake data for pages, events, and user activities using existing properties."

    def add_arguments(self, parser):
        parser.add_argument(
            "total_pages",
            type=int,
            help="Indicates the number of fake pages to be created.",
        )
        parser.add_argument(
            "events_per_page", type=int, help="Indicates the number of events per page."
        )
        parser.add_argument(
            "user_activities_per_page",
            type=int,
            help="Indicates the number of user activities per page.",
        )

    def handle(self, *args, **kwargs):
        total_pages = kwargs["total_pages"]
        events_per_page = kwargs["events_per_page"]
        user_activities_per_page = kwargs["user_activities_per_page"]
        fake = Faker()

        # Get all existing properties from the database
        properties = Property.objects.all()

        event_actions = (
            "click",
            "mouseenter",
            "mouseleave",
            "mousemove",
            "mouseover",
            "mousedown",
            "keydown",
            "keyup",
            "keypress",
            "abort",
            "change",
            "dblclick",
            "drag",
            "drop",
        )

        for property in properties:
            for _ in range(total_pages):
                path = fake.uri_path()
                page = Page.objects.create(
                    website=property,
                    path=path,
                    referer=fake.uri(),
                    user_agent=fake.user_agent(),
                    ip_address=fake.ipv4(),
                )

                for _ in range(events_per_page):
                    Event.objects.create(
                        page=page,
                        timestamp=fake.date_time_this_month(),
                        category=random.choice(("interaction", "conversion")),
                        action=random.choice(event_actions),
                        label=fake.word(),
                    )

                for _ in range(user_activities_per_page):
                    action = random.choice(event_actions)
                    session_id = fake.uuid4()
                    UserActivity.objects.create(
                        website=property,
                        action=action,
                        session_id=session_id,
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully populated pages, events, and user activities using existing properties."
            )
        )
