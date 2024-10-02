

import os
import pandas as pd
from PyPDF2 import PdfReader
from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
from django.conf import settings
import re

def extract_text_from_pdf(pdf_path):# Extracts text from  PDF
    reader = PdfReader(pdf_path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    return extracted_text


def process_extracted_text(extracted_text):
    lines = extracted_text.split('\n')
    data = {
        "Item": [],
        "Cost": [],
        "Description": []
    }
    
    current_item = None
    current_description = []
    
    for line in lines:
        
        line = line.strip()

        
        if not line:
            continue

        cost_match = re.search(r'(\d+(\.\d{1,2})?)$', line)
        
        if cost_match:
            
            current_cost = cost_match.group(1)
            item_and_cost = line[:cost_match.start()].strip()

            
            if not item_and_cost.endswith(' '): 
                item_and_cost = re.sub(r'(\D+)(\d+(\.\d{1,2})?)$', r'\1', line)  # Separate item from cost

            current_item = item_and_cost.strip()

            
            current_description_text = " ".join(current_description).strip() if current_description else "N/A"

            # data structure
            if current_item:
                data["Item"].append(current_item)
                data["Cost"].append(current_cost)
                data["Description"].append(current_description_text)

            
            current_description = []
        else:
           
            if current_item:
                current_description.append(line)

    
    if current_item and current_description:
        data["Item"].append(current_item)
        data["Cost"].append("N/A")
        data["Description"].append(" ".join(current_description).strip())

    return data

def generate_excel_from_data(data, pdf_name):
   
    df = pd.DataFrame(data)
    excel_dir = os.path.join(settings.MEDIA_ROOT, 'excel')

   
    if not os.path.exists(excel_dir):
        os.makedirs(excel_dir)

    excel_filename = pdf_name.replace('.pdf', '.xlsx')
    excel_path = os.path.join(excel_dir, excel_filename)
    df.to_excel(excel_path, index=False)

    return excel_filename

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()  # Save PDF file
            pdf_path = os.path.join(settings.MEDIA_ROOT, document.pdf_file.name)
            
            extracted_text = extract_text_from_pdf(pdf_path)

            print('--------------------------------------',extracted_text,'-----------------------------------extracted_text')
            print('\n')
            
            structured_data = process_extracted_text(extracted_text)
            print('----------------------------',structured_data,'----------------------------------------------structured_data')
          
            excel_filename = generate_excel_from_data(structured_data, document.pdf_file.name)
            
            # Step 4: Save the generated Excel file path to the model
            document.excel_file = f'excel/{excel_filename}'
            document.save()
            
            # Step 5: Redirect to preview the Excel file
            return redirect('document_preview', document_id=document.id)
    else:
        form = DocumentForm()
    return render(request, 'upload_document.html', {'form': form})

def document_preview(request, document_id):
    document = Document.objects.get(id=document_id)
    
  
    excel_path = os.path.join(settings.MEDIA_ROOT, document.excel_file.name)
    df = pd.read_excel(excel_path)
    
   
    preview_data = list(zip(df['Item'], df['Cost'], df['Description']))
    
    return render(request, 'document_preview.html', {
        'document': document,
        'preview_data': preview_data
    })

from django.http import FileResponse
from django.shortcuts import get_object_or_404

def download_excel(request, document_id):
   
    document = get_object_or_404(Document, id=document_id)
  
    excel_path = os.path.join(settings.MEDIA_ROOT, document.excel_file.name)
   
    response = FileResponse(open(excel_path, 'rb'), as_attachment=True, filename=os.path.basename(excel_path))
    return response
