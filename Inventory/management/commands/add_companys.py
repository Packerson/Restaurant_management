from django.core.management.base import BaseCommand

from ._private import add_companys


class Command(BaseCommand):
    help = "added company's"

    def handle(self, *args, **options):
        add_companys()
        self.stdout.write(self.style.SUCCESS("Successfully add company's"))
