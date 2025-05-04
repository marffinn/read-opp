#!/usr/bin/env python3
"""
Web interface for the PDF CRM Opportunity Extractor.

This application provides a web interface for uploading PDF files
and extracting CRM opportunity data using a local LLM.
"""

import os
import json
import tempfile
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

# Import our CRM extractor modules
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.pdf_processor.loader import PDFLoader
from src.crm_extractor.extractor import CRMDataExtractor, CRMOpportunity

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages and session
Bootstrap(app)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the home page with the upload form."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and extraction."""
    # Check if a file was uploaded
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)
    
    file = request.files['file']
    
    # Check if the file was selected
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(request.url)
    
    # Check if the file is allowed
    if file and allowed_file(file.filename):
        # Save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Process the PDF
            loader = PDFLoader()
            documents = loader.load(filepath)
            
            # Extract CRM data
            extractor = CRMDataExtractor()
            crm_data = extractor.extract(documents)
            
            # Store the results in the session
            session['extraction_results'] = crm_data.model_dump()
            session['filename'] = filename
            
            # Redirect to results page
            return redirect(url_for('results'))
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'danger')
            return redirect(url_for('index'))
    else:
        flash('File type not allowed. Please upload a PDF file.', 'danger')
        return redirect(url_for('index'))

@app.route('/results')
def results():
    """Display the extraction results."""
    # Check if results exist in session
    if 'extraction_results' not in session:
        flash('No extraction results found. Please upload a PDF file.', 'warning')
        return redirect(url_for('index'))
    
    # Get results from session
    results = session['extraction_results']
    filename = session.get('filename', 'Unknown file')
    
    # Render results template
    return render_template('results.html', results=results, filename=filename)

@app.route('/batch')
def batch():
    """Render the batch processing page."""
    # Get list of PDF files in the uploads folder
    pdf_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) 
                if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f)) 
                and f.lower().endswith('.pdf')]
    
    return render_template('batch.html', pdf_files=pdf_files)

@app.route('/process_batch', methods=['POST'])
def process_batch():
    """Process multiple PDF files."""
    # Get selected files
    selected_files = request.form.getlist('selected_files')
    
    if not selected_files:
        flash('No files selected', 'warning')
        return redirect(url_for('batch'))
    
    results = []
    
    # Process each selected file
    for filename in selected_files:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            # Process the PDF
            loader = PDFLoader()
            documents = loader.load(filepath)
            
            # Extract CRM data
            extractor = CRMDataExtractor()
            crm_data = extractor.extract(documents)
            
            # Add to results
            result = crm_data.model_dump()
            result['filename'] = filename
            results.append(result)
            
        except Exception as e:
            flash(f'Error processing {filename}: {str(e)}', 'danger')
    
    # Store batch results in session
    session['batch_results'] = results
    
    # Redirect to batch results page
    return redirect(url_for('batch_results'))

@app.route('/batch_results')
def batch_results():
    """Display batch processing results."""
    # Check if results exist in session
    if 'batch_results' not in session:
        flash('No batch results found. Please process files first.', 'warning')
        return redirect(url_for('batch'))
    
    # Get results from session
    results = session['batch_results']
    
    # Render batch results template
    return render_template('batch_results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
