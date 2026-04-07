from django.core.management.base import BaseCommand

from handling_time.models import HandlingTimeConfig
from handling_time.services import calculate_handling_time
from integrations.allegro.exceptions import AllegroError
from integrations.allegro.service import update_handling_time


class Command(BaseCommand):
    help = "Update handling time for all configures offers"

    def handle(self, *args, **options):
        configs = HandlingTimeConfig.objects.all()

        if not configs.exists():
            self.stdout.write("No configs found")
            return

        for config in configs:
            try:
                handling_time = calculate_handling_time(config.target_date)
                update_handling_time(
                    config.account,
                    config.offer_id,
                    handling_time
                )
                self.stdout.write(
                    f"OK: {config.offer_id} -> {handling_time}"
                )
            except AllegroError as e:
                self.stdout.write(
                    f"Error: {config.offer_id} -> {str(e)}"
                )
            except Exception as e:
                self.stdout.write(
                    f"UNEXPECTED error: {config.offer_id} -> {str(e)}"
                )