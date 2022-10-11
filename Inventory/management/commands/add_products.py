from django.core.management.base import BaseCommand

from ._private import add_products


class Command(BaseCommand):
    help = 'added products'

    def handle(self, *args, **options):
        add_products()
        self.stdout.write(self.style.SUCCESS("Successfully add products"))
