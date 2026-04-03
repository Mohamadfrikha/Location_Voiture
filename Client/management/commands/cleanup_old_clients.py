from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from Client.models import Client

class Command(BaseCommand):
    help = 'Supprime les comptes non activés depuis plus de 7 jours'

    def handle(self, *args, **options):
        old_clients = Client.objects.filter(
            is_active=False,
            date_inscription__lt=timezone.now() - timedelta(hours=24)
        )
        count = old_clients.count()
        old_clients.delete()
        self.stdout.write(f"{count} comptes supprimés.")