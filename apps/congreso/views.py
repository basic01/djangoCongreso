from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from apps.congreso.models import Participante, Detalle, Programa, Taller, Inscripcion
from apps.congreso.forms import ParticipanteForm, InscripcionForm, AdminGeneralForm, AdminTalleresForm, AdminProgramaForm, AdminInscripcionesForm
from django.views.generic import ListView
from django.contrib import messages

def inicio(request):
	contexto = {
		'detalles': Detalle.objects.first(),
	}
	return render(request, 'congreso/index.html', contexto)		

def registro(request):
	if request.method == 'POST':
		form = ParticipanteForm(request.POST)
		if form.is_valid():
			data = request.POST.copy()
			n = data.get('nombre')
			aP = data.get('apellidoPaterno')
			aM = data.get('apellidoMaterno')
			c = data.get('correo')
			existenciaParticipante = Participante.objects.filter(nombre=n,apellidoPaterno=aP, apellidoMaterno=aM, correo=c)
			if(existenciaParticipante):
				messages.error(request, 'Ya estás registrado')
			else:
				form.save()
				messages.success(request, 'Registro exitoso')
			form = ParticipanteForm()
			#return redirect('taller:tallerExito', "r")
	else:
		form = ParticipanteForm()
	return render(request, 'congreso/registro.html', {'title':'Registro', 'form': form})

def exito(request, tipoExito):
	if tipoExito != 'r' and tipoExito != 'i':
		return redirect('taller:tallerInicio')	
	return render(request, 'congreso/exito.html',{'title':'Success','tipoExito': tipoExito})	


def talleres(request):
	detalles = {
		'title': 'Talleres',
		'jueves1': Taller.objects.filter(dia='jueves', horario='12:00 - 14:30'),
		'jueves2': Taller.objects.filter(dia='jueves', horario='17:10 - 19:30'),
		'viernes': Taller.objects.filter(dia='viernes', horario='11:00 - 13:30'),
	}
	return render(request, 'congreso/talleres.html', detalles)

def programa(request):
	detalles = {
		'request':request,
		'jueves': Programa.objects.filter(dia='jueves').order_by('horario'),
		'viernes': Programa.objects.filter(dia='viernes').order_by('horario'),
		'title':'Programa',
	}
	return render(request, 'congreso/programa.html', detalles )

def warning(request, i, t, bandera):
	inscripcion = Inscripcion.objects.get(id=i)
	viejoT = Taller.objects.get(id=inscripcion.idTaller.id)
	if bandera == 1:
		taller = Taller.objects.get(id=t)
		inscripcion.taller = taller.nombre
		inscripcion.save()
		taller.inscripcion_set.add(inscripcion)
		taller.cupo = taller.cupo-1
		taller.save()
		viejoT.cupo = viejoT.cupo+1
		viejoT.save()
		messages.success(request, 'Cambios guardados exitosamente')
		detalles = {
			'title':'Programa',
			'i': i,
			't': t,
		}
	else:
		detalles = {
			'title':'Programa',
			'i': i,
			't': t,
			'taller': inscripcion.taller,
		}
	return render(request, 'congreso/warning.html',detalles)	


def inscripcion(request, idTaller):
	#taller = Taller.objects.get(id=idTaller)
	taller = get_object_or_404(Taller, id=idTaller)
	details = Detalle.objects.get(id=1)
	cupoMax = details.cupoMax
	if request.method == 'GET':
		form = InscripcionForm()
		detalles = {
			'title': 'Inscripción',
			'taller': taller,
			'form': form,
		}
	if request.method == 'POST':
		form = InscripcionForm(request.POST)
		if form.is_valid():
			if(taller.cupo>0 and taller.cupo<=cupoMax):
				data = request.POST.copy()
				n = data.get('nombre')
				aP = data.get('apellidoPaterno')
				aM = data.get('apellidoMaterno')
				existenciaParticipante = Participante.objects.filter(nombre=n,apellidoPaterno=aP, apellidoMaterno=aM)
				if(existenciaParticipante):
					
					inscritoTaller = Inscripcion.objects.filter(taller=taller.nombre, nombre=n,apellidoPaterno=aP, apellidoMaterno=aM)
					if(inscritoTaller):
						messages.error(request, 'Ya estás registrado en este taller')
						#Ya está registrado en este taller
					else:
						inscrito = Inscripcion.objects.filter(horario=taller.horario,nombre=n,apellidoPaterno=aP, apellidoMaterno=aM)
						p = Participante.objects.get(nombre=n,apellidoPaterno=aP, apellidoMaterno=aM)
						if(inscrito):
							#i = Inscripcion.objects.get(horario=taller.horario,nombre=n,apellidoPaterno=aP, apellidoMaterno=aM)
							i = Inscripcion.objects.get(horario=taller.horario,nombre=n,apellidoPaterno=aP, apellidoMaterno=aM)
							return redirect('taller:tallerWarning', i.id, taller.id, 0)
							#Ya estás registrado en un taller del mismo horario
						else:
							nuevaI = Inscripcion(taller=taller.nombre, dia=taller.dia, horario=taller.horario,nombre=n, apellidoPaterno=aP, apellidoMaterno=aM)
							nuevaI.save()
							taller.inscripcion_set.add(nuevaI)
							p.inscripcion_set.add(nuevaI)
							taller.cupo = taller.cupo-1
							taller.save()
							messages.success(request, 'Inscripción exitosa')
							#Inscripción exitosa
				else:
					messages.error(request, 'Todavía no estás registrado')
					#return HttpResponse(detalles['validacion'])
					#messages.warning(request, detalles['participante'].nombre)
					#Usuario no existe
			else:
				messages.error(request, 'Ya no hay cupo para este taller')
				#Cupo límite
			return redirect('taller:tallerInscripcion', idTaller)
	return render(request, 'congreso/inscripcion.html', detalles)


#Páginas administrador

def administradorInicio(request):
	return render(request, 'localadmin/index.html')

class ViewParticipantes(ListView):
	model = Participante
	queryset = Participante.objects.order_by('apellidoPaterno','apellidoMaterno','nombre')
	template_name = 'localadmin/participantes.html'
	detalles = {
		'title': 'Participantes Admin',
	}

def participantesMondragon(request):
	contexto = {
		'participantes': Participante.objects.filter(mondragon = 'sí'),
		'title': 'Participantes Mondragón',
	}
	return render(request, 'localadmin/participantesMondragon.html', contexto)	

class ViewPrograma(ListView):
	model = Programa
	queryset = Programa.objects.order_by('dia','horario')
	template_name = 'localadmin/programa.html'
	detalles = {
		'title': 'Programa Admin',
	}

class ViewTalleres(ListView):
	model = Taller
	queryset = Taller.objects.order_by('dia','horario','nombre')
	template_name = 'localadmin/talleres.html'
	detalles = {
		'title': 'Talleres Admin',
	}

class ViewInscripciones(ListView):
	model = Inscripcion
	queryset = Inscripcion.objects.order_by('dia','horario', 'taller', 'apellidoPaterno','apellidoMaterno','nombre')
	template_name = 'localadmin/inscripciones.html'
	detalles = {
		'title': 'Insripciones Admin',
	}
