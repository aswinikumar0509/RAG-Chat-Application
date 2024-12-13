from django.shortcuts import render,redirect
from .forms import PDFUploadForm
from .models import PDFUpload
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant
from langchain_community.vectorstores import Qdrant
from dotenv import load_dotenv
import os
import numpy as np
# Create your views here.

load_dotenv()

def upload_pdf(request):

    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_instance = PDFUpload(pdf_file=form.cleaned_data['pdf_file'])
            pdf_instance.save()
            loader = PyPDFLoader(pdf_instance.pdf_file.path)
            documents=loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            chunks = text_splitter.split_documents(documents)
            # texts.save()

            # Now initalizing embedding model using huggingface
            embedding_model = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

            # connect to Qdrant
            qdrant_url = os.getenv('QDRANT_URL')
            qdrant_api_key = os.getenv('QDRANT_API_KEY')
            qdrant_collection_name = "pdf_chunks"

            # Create or connect to the qdrant vector store

            vectorstore = Qdrant(
                embeddings = embedding_model,
                collection_name=qdrant_collection_name,
                url = qdrant_url,
                api_key=qdrant_api_key,

            )

            for chunk in chunks:
                vectorstore.add_texts([chunk.page_content])


            return redirect('upload_success')
    else:
        form = PDFUploadForm()
    return render(request, 'chatsystem/upload_pdf.html', {'form': form})


#  function for the showing the result

def query_pdf(request):
    results = []

    if request.method=='POST':
        form = PDFUploadForm(request.form)

        if form.is_valid():
            user_query = form.cleaned_data['query']

            # Connect to Qdrant for querying
            qdrant_url = os.getenv('QDRANT_URL')
            qdrant_api_key = os.getenv('QDRANT_API_KEY')
            qdrant_collection_name = "pdf_chunks"

            vectorstore = Qdrant(
                embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2'),
                collection_name=qdrant_collection_name,
                url = qdrant_url,
                api_key=qdrant_api_key

            )

            # Perform similarity search in qdrant
            results = vectorstore.similarity_search(user_query)

        else:
            form = PDFUploadForm()

    return render(request , 'chatsystem/query_pdf.html',{'form':form , 'results':results})


def upload_success(request):
    return render(request, 'chatsystem/upload_success.html')
