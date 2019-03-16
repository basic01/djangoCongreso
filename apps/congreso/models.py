from django.db import models

class Participante(models.Model):
	CHOICES = [
			('sí', 'Sí'),
			('no', 'No'),			
		]
	nombre = models.CharField(max_length=100)
	apellidoPaterno = models.CharField(max_length=100)
	apellidoMaterno = models.CharField(max_length=100)
	correo = models.EmailField(max_length=100)
	institucion = models.CharField(max_length=200)
	mondragon = models.CharField(choices=CHOICES, max_length=2)
	#date_posted = models.DateTimeField(default=timezone.now)

class Detalle(models.Model):
	lugar = models.CharField(max_length=100)
	fecha = models.CharField(max_length=100)
	hora = models.CharField(max_length=50)
	direccion = models.CharField(max_length=150)
	telefono = models.CharField(max_length=20)
	telefono2 = models.CharField(max_length=20)
	correo = models.EmailField(max_length=100)
	cupoMax = models.IntegerField()
	#descripcion = models.TextField()

class Taller(models.Model):
	dia = models.CharField(max_length=50)
	horario = models.CharField(max_length=50)
	nombre = models.CharField(max_length=200)
	ponente = models.CharField(max_length=100)
	cupo = models.IntegerField()

class Programa(models.Model):
	dia = models.CharField(max_length=50)
	horario = models.CharField(max_length=50)
	actividad = models.CharField(max_length=200)

class Inscripcion(models.Model):
	idTaller = models.ForeignKey(Taller, null=True, blank=True, on_delete=models.CASCADE)
	taller = models.CharField(max_length=200)
	dia = models.CharField(max_length=50)
	horario = models.CharField(max_length=50)
	idParticipante = models.ForeignKey(Participante, null=True, blank=True, on_delete=models.CASCADE)
	nombre = models.CharField(max_length=100)
	apellidoPaterno = models.CharField(max_length=100)
	apellidoMaterno = models.CharField(max_length=100)
