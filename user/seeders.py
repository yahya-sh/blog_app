from user.tests.factories import UserFactory
from scripts.seed.registry import register
from scripts.seed.base import BaseSeeder
from django.contrib.auth import get_user_model


@register
class UserSeeder(BaseSeeder):

    @classmethod
    def add_arguments(cls, parser):
        parser.add_argument("--users-count", type=int, default=20)

    def run(self, **options):
        User = get_user_model()

        # ----------------------------
        # 1. Ensure admin user exists
        # ----------------------------
        admin_username = "admin"
        admin_email = "admin@blog.com"
        admin_password = "admin"

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
            )
            print("✔ Created admin/admin user")
        else:
            print("✔ Admin user already exists")

        # ----------------------------
        # 2. Create fake users
        # ----------------------------
        UserFactory.create_batch(options["users_count"])