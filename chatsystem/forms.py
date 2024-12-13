from django import forms

class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField()
    query = forms.CharField(max_length=1000)