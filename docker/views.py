from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import PDFUploadForm
import fitz  # PyMuPDF para manejar PDF
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class PDFUploadView(FormView):
    template_name = 'subirPDF.html'
    form_class = PDFUploadForm
    success_url = reverse_lazy('viewPDF')

    def form_valid(self, form):
        archivo_pdf = self.request.FILES['archivo_pdf']
        return self.render_to_response(self.get_context_data(archivo_pdf=archivo_pdf))

@csrf_exempt
def viewPDF(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        if pdf_file:
            save_path = os.path.join(BASE_DIR, 'MEDIA', 'archivo.pdf')
            print("Archivo guardado en:", save_path)

            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Guarda el archivo en el servidor
            with open(save_path, 'wb+') as destino:
                for chunk in pdf_file.chunks():
                    destino.write(chunk)

            texto_buscado = "FIRMA1AQUI"
            encontrado, coordenadas = buscar_texto_en_pdf(save_path, texto_buscado)

            if encontrado:
                nuevo_pdf = agregar_imagen_a_pdf(save_path, coordenadas, os.path.join(BASE_DIR, 'MEDIA', 'firmaEloy.jpg'))
                return HttpResponse(f"Archivo PDF subido con éxito, texto encontrado y reemplazado. Nuevo archivo: {nuevo_pdf}")
            else:
                return HttpResponse(f"Archivo PDF subido con éxito pero el texto '{texto_buscado}' no fue encontrado.")
        else:
            return HttpResponse("No se ha subido ningún archivo PDF.")
    return render(request, 'subirPDF.html')

def buscar_texto_en_pdf(ruta_pdf, texto_a_buscar):
    doc = fitz.open(ruta_pdf)
    for pagina in doc:
        areas = pagina.search_for(texto_a_buscar)
        if areas:
            return True, areas[0]  # Devuelve las coordenadas del área del texto
    return False, None

def agregar_imagen_a_pdf(ruta_pdf, coordenadas, ruta_imagen):
    doc = fitz.open(ruta_pdf)
    pagina = doc.load_page(0)  # Carga la primera página del PDF

    # Obtenemos el rectángulo del texto (coordenadas)
    rect = fitz.Rect(coordenadas)

    # Calculamos el ancho del área de texto (no cambiamos la altura)
    ancho_texto = rect.width

    # Insertar la imagen, ajustando solo al ancho del área del texto y manteniendo proporción
    pagina.insert_image(rect, filename=ruta_imagen, keep_proportion=True, width=ancho_texto)

    # Guardar el nuevo archivo PDF
    nuevo_pdf = os.path.join(BASE_DIR, 'MEDIA', 'archivo_modificado.pdf')
    doc.save(nuevo_pdf)
    doc.close()

    return nuevo_pdf