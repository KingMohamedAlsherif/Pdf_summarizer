from django.shortcuts import render, redirect
from .forms import PDFUploadForm
from .models import PDFDocument
from .utils import extract_text_from_pdf, summarize_text

"""
PDF Document Views
----------------
This module handles the web views for PDF upload and summary display functionality.
It provides interfaces for users to upload PDF documents and view their summaries.
"""

def upload_pdf(request):
    """
    Handle PDF file uploads and generate summaries.
    
    Parameters:
        request: HttpRequest object containing metadata about the request
        
    Returns:
        HttpResponse: Rendered upload form or redirects to summary view
        
    Flow:
        1. If POST request: Process form submission
        2. If valid: Save PDF, extract text, generate summary
        3. If GET request: Display empty upload form
    """
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded PDF document
            pdf_document = form.save()
            pdf_path = pdf_document.pdf_file.path
            
            # Extract text from PDF
            text = extract_text_from_pdf(pdf_path)
            
            # Generate and save summary if text extraction succeeded
            if not text.startswith("Error"):
                summary = summarize_text(text)
                pdf_document.summary = summary
                pdf_document.save()
            
            # Redirect to the summary view page
            return redirect('view_summary', pk=pdf_document.pk)
    else:
        # Display empty form for GET requests
        form = PDFUploadForm()
    return render(request, 'summarizer/upload.html', {'form': form})

def view_summary(request, pk):
    """
    Display the summary of a processed PDF document.
    
    Parameters:
        request: HttpRequest object
        pk (int): Primary key of the PDFDocument to display
        
    Returns:
        HttpResponse: Rendered template with the document summary
    """
    # Retrieve the document and display its summary
    document = PDFDocument.objects.get(pk=pk)
    return render(request, 'summarizer/summary.html', {'document': document})