from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from reportes.models import Visita

class Command(BaseCommand):
    help = 'Elimina registros de visitas Anteriores a 60 dias'

    def handle(self, *args, **options):
        oldVisitas = Visita.objects.filter(timestamp__lte= datetime.now() - timedelta(days = 60))
        oldVisitas.delete()
        self.stdout.write(self.style.SUCCESS('Registros de Visitas Eliminados Satisfactoriamente'))
