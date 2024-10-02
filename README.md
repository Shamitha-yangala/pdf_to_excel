# pdf_to_excel

# Restaurant Menu PDF to Excel Converter

## Overview

The **Restaurant Menu PDF to Excel Converter** is a Django web application designed to help restaurant owners and managers convert their menu PDFs into Excel files. This tool extracts menu items, prices, and descriptions from uploaded PDF menus and organizes them in a clean Excel format. It's an easy-to-use solution for digitizing and managing restaurant menus.

## Features

- Upload restaurant menu PDFs.
- Extract menu items and prices from the PDF.
- Generate an Excel (.xlsx) file with structured data.
- Preview extracted data before downloading.
- Download the Excel file for further use.
  
## Technologies Used

- **Backend**:
  - Python 3.x
  - Django 5.1.1
  - PyPDF2
  - Pandas
  - OpenPyXL
- **Frontend**:
  - HTML5, CSS3, JavaScript
- **Database**:
  - SQLite (Default Django database, can be swapped for PostgreSQL/MySQL)
  
## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Setup Instructions

1. Clone the repository:
    git clone https://github.com/yourusername/restaurant-menu-converter.git
    cd restaurant-menu-converter
   
2. Create a virtual environment:
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
   

3. Install the required packages:
    pip install -r requirements.txt


4. Apply database migrations:
    python manage.py migrate

5. Run the development server:
    python manage.py runserver


6. Access the application at `http://127.0.0.1:8000/`.

## Usage

1. Go to the home page and upload a restaurant menu PDF.
2. After processing, you can preview the extracted data (menu items, prices).
3. Download the Excel file containing the structured menu data.
