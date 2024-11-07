from django.shortcuts import render,redirect
from .forms import PDFUploadForm
from .models import PDFUpload
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Create your views here.

def upload_pdf(request):

    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_instance = PyPDFLoader(form)
            loader = pdf_instance.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            texts = text_splitter.split_documents(loader)
            texts.save()
            return redirect('upload_success')
    else:
        form = PDFUploadForm()
    return render(request, 'chatsystem/upload_pdf.html', {'form': form})


def upload_success(request):
    return render(request, 'chatsystem/upload_success.html')
