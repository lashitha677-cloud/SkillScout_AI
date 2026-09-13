import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create the initial admin user from environment variables."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.getenv("ADMIN_USERNAME")
        password = os.getenv("ADMIN_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "ADMIN_USERNAME or ADMIN_PASSWORD is not set."
                )
            )
            return

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.SUCCESS(
                    "A superuser already exists. No changes made."
                )
            )
            return

        user = User.objects.create_superuser(
            username=username,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Superuser '{user.username}' created successfully."
            )
        )