from django.db import models
from django.conf import settings
from .signals import visitaSignal

# Create your models here.

User = settings.AUTH_USER_MODEL

class Visita(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    ip_address = models.CharField(max_length=220, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "%s visited on %s" %(self.user, self.timestamp)

# Obtener direccion IP
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", None)
    return ip

# Recibidor del signal
def visitaReceiver(request, *args, **kwargs):
    if request.user.is_authenticated:
        user_ = request.user
    else:
        user_ = None
    visita = Visita.objects.create(
        user = user_,
        ip_address = get_ip(request),
    )

# Conectar signal
visitaSignal.connect(visitaReceiver)