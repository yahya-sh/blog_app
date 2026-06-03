from django.core.management.base import BaseCommand
from user.tests.factories import UserFactory


class Command(BaseCommand):
    help = "Seed fake users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=20,
            help="Number of users to create",
        )

    def handle(self, *args, **options):
        count = options["count"]

        self.stdout.write(f"Creating {count} users...")

        UserFactory.create_batch(count)

        self.stdout.write(self.style.SUCCESS(f"Created {count} users"))