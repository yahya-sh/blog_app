import random
from django.contrib.auth import get_user_model
from blog.tests.factories import BlogFactory
from scripts.seed.registry import register
from scripts.seed.base import BaseSeeder


@register
class BlogSeeder(BaseSeeder):
    depends_on = ["user"]

    @classmethod
    def add_arguments(cls, parser):
        parser.add_argument("--blogs-count", type=int, default=50)

    def run(self, **options):
        users = list(get_user_model().objects.all())

        if not users:
            print("No users found. Skipping blog seeding.")
            return
        
        for _ in range(options["blogs_count"]):
            BlogFactory.create(author=random.choice(users))