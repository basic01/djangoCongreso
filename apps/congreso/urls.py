from django.urls import path
from . import views

app_name = 'taller'

urlpatterns = [
	path('', views.inicio, name='tallerInicio'),
	path('registro', views.registro, name='tallerRegistro'),
	path('programa', views.programa, name='tallerPrograma'),
	path('talleres', views.talleres, name='tallerTalleres'),
	path('success/<str:tipoExito>', views.exito, name='tallerExito'),
	path('warning/<int:i>-<int:t>/<int:bandera>', views.warning, name='tallerWarning'),
	path('inscripcion/<int:idTaller>', views.inscripcion, name='tallerInscripcion'),

	path('manage', views.administradorInicio, name="administradorInicio"),
	path('manage/participantes', views.ViewParticipantes.as_view(), name="administradorParticipantes"),
	path('manage/participantesMondragon', views.participantesMondragon, name="administradorParticipantesMondragon"),
	path('manage/programa', views.ViewPrograma.as_view(), name="administradorPrograma"),
	path('manage/talleres', views.ViewTalleres.as_view(), name="administradorTalleres"),
	path('manage/inscripciones', views.ViewInscripciones.as_view(), name="administradorInscripciones"),
]