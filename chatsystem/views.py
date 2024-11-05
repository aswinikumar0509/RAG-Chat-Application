from django.shortcuts import render,redirect
from .forms import PDFUploadForm
from .models import PDFUpload
from langchain_community.document_loaders import PyPDFLoader

# Create your views here.

def upload_pdf(request):

    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_instance = PyPDFLoader(form)
            loader = pdf_instance.load()
            loader.save()
            return redirect('upload_success')
    else:
        form = PDFUploadForm()
    return render(request, 'upload_pdf.html', {'form': form})


def upload_success(request):
    return render(request, 'upload_success.html')
