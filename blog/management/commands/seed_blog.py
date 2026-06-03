import random
from django.core.management.base import BaseCommand
from blog.tests.factories import TagFactory, BlogFactory
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Seed fake blogs + tags"

    def add_arguments(self, parser):
        parser.add_argument(
            "--blogs",
            type=int,
            default=50,
        )
        parser.add_argument(
            "--tags",
            type=int,
            default=10,
        )
        parser.add_argument(
            "--published-ratio",
            type=float,
            default=0.7,
        )

    def handle(self, *args, **options):
        blogs_count = options["blogs"]
        tags_count = options["tags"]
        published_ratio = options["published_ratio"]

        User = get_user_model()
        users = list(User.objects.all())

        if not users:
            self.stdout.write(
                self.style.ERROR("No users found. Run user_seed first.")
            )
            return

        self.stdout.write(f"Creating {tags_count} tags...")
        TagFactory.create_batch(tags_count)

        published_count = int(blogs_count * published_ratio)
        draft_count = blogs_count - published_count

        self.stdout.write(f"Creating {published_count} published blogs...")
        for _ in range(published_count):
            BlogFactory(
                author=random.choice(users),
                published_blog=True,
            )

        self.stdout.write(f"Creating {draft_count} draft blogs...")
        for _ in range(draft_count):
            BlogFactory(
                author=random.choice(users),
            )

        self.stdout.write(self.style.SUCCESS("Blog seeding complete"))