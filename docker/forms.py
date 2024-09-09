from django import forms

class PDFUploadForm(forms.Form):
    archivo_pdf = forms.FileField(
        required=True,
        label='Subir PDF',
        widget=forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
    )
