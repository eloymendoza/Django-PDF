from django.urls import path
from .views import PDFUploadView, viewPDF  # Asegúrate de que estas vistas estén importadas correctamente

urlpatterns = [
    path('', PDFUploadView.as_view(), name='viewPDF'),  # Asegúrate de llamar a as_view()
    path('otra', viewPDF, name='otraVista'),  # Cambié el nombre a 'otraVista' para evitar conflicto con el nombre anterior
]
