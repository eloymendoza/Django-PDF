from django.db import models

class TuModelo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    archivo_pdf = models.FileField(upload_to='pdfs/')  # La carpeta 'pdfs/' será donde se guarden los archivos

    def __str__(self):
        return self.nombre