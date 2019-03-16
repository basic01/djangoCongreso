from django.contrib import admin
from apps.congreso.models import Participante, Detalle, Taller, Programa, Inscripcion
# Register your models here.
admin.site.register(Participante)
admin.site.register(Detalle)
admin.site.register(Taller)
admin.site.register(Programa)
admin.site.register(Inscripcion)
