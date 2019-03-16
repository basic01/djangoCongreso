from django import forms
from apps.congreso.models import Participante, Inscripcion, Taller, Detalle, Programa

class ParticipanteForm(forms.ModelForm):
	class Meta:
		model = Participante
		fields = (
			'nombre',
			'apellidoPaterno',
			'apellidoMaterno',
			'correo',
			'institucion',
			'mondragon',
		)

		labels = {
			'apellidoPaterno': 'Apellido Paterno:',
			'apellidoMaterno': 'Apellido Materno:',
			'mondragon': '¿Eres estudiante o docente de la Universidad Mondragón?',
		}


class InscripcionForm(forms.ModelForm):
	class Meta:
		model = Inscripcion

		fields = (
				'nombre',
				'apellidoPaterno',
				'apellidoMaterno',
			)

		labels = {
			'apellidoPaterno': 'Apellido Paterno:',
			'apellidoMaterno': 'Apellido Materno:',
		}

class AdminGeneralForm(forms.ModelForm):
	class Meta:
		model = Detalle

		fields = (
				'lugar',
				'fecha',
				'hora',
				'direccion',
				'telefono',
				'telefono2',
				'correo',
				'cupoMax'
			)

class AdminInscripcionesForm(forms.ModelForm):
	class Meta:
		model = Inscripcion
		fields = (
				'taller',
				'dia',
				'horario',
				'nombre',
				'apellidoPaterno',
				'apellidoMaterno',
			)

class AdminTalleresForm(forms.ModelForm):
	class Meta:
		model =Taller

		fields = (
				'dia',
				'horario',
				'nombre',
				'ponente',
				'cupo',
			)
class AdminProgramaForm(forms.ModelForm):
	class Meta:
		model = Programa

		fields = (
				'dia',
				'horario',
				'actividad'
			)