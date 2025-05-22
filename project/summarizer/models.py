from django.db import models


class PDFDocument(models.Model):
    title = models.CharField(max_length=200) # Title of the PDF
    pdf_file = models.FileField(upload_to='pdfs/') # File field to upload the PDF
    uploaded_at = models.DateTimeField(auto_now_add=True) # Timestamp when the PDF was uploaded
    summary = models.TextField(blank=True) # Summary of the PDF content

    def __str__(self):
        return self.title