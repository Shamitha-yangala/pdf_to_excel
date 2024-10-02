from django.db import models



class Document(models.Model):
    pdf_file = models.FileField(upload_to='pdf/')
    excel_file = models.FileField(upload_to='excel/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.pdf_file.name
