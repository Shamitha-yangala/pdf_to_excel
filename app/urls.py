
from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_document, name='upload_document'),
    path('preview/<int:document_id>/', views.document_preview, name='document_preview'),
    path('download/<int:document_id>/', views.download_excel, name='download_excel'), 
]
