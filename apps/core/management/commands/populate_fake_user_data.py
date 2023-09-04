# Import necessary modules
import random

from django.core.management.base import BaseCommand
from faker import Faker

from apps.core.models import Property, UserActivity


class Command(BaseCommand):
    help = "Populates the UserActivity model with Faker data."

    def add_arguments(self, parser):
        parser.add_argument(
            "total_records",
            type=int,
            help="Indicates the number of fake records to be created.",
        )

    def handle(self, *args, **kwargs):
        total_records = kwargs["total_records"]
        fake = Faker()

        # Create a dictionary to keep track of unique combinations of path and IP per website
        unique_combinations = {}

        paths = [fake.uri_path() for _ in range(5)]

        # Get all existing properties from the database
        properties = Property.objects.all()

        for _ in range(total_records):
            # Randomly select a property
            property = random.choice(properties)

            # Generate a unique combination of path and IP for each property
            while True:
                path = random.choice(paths)
                ip_address = fake.ipv4()
                unique_key = f"{property.id}-{path}-{ip_address}"

                if unique_key not in unique_combinations:
                    unique_combinations[unique_key] = True
                    break

            # Create a UserActivity record
            UserActivity.objects.create(
                website=property,
                user_agent=fake.user_agent(),
                timestamp=fake.date_time_this_month(),
                path=path,
                ip_address=ip_address,
                city=fake.city(),
                country=fake.country(),
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully populated {total_records} UserActivity records with Faker data."
            )
        )
