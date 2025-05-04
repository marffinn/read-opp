#!/usr/bin/env python3
"""
Example script demonstrating how to use the PDF CRM Extractor programmatically.
"""

import sys
import os
import json

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pdf_processor.loader import PDFLoader
from src.crm_extractor.extractor import CRMDataExtractor

def main():
    """Run the example extraction."""
    # Check if a PDF file path was provided
    if len(sys.argv) < 2:
        print("Usage: python extract_example.py path/to/pdf_file.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]

    try:
        # Load the PDF
        print(f"Loading PDF: {pdf_path}")
        loader = PDFLoader()
        documents = loader.load(pdf_path)

        print(f"Loaded {len(documents)} pages from the PDF")

        # Extract CRM data
        print("Extracting CRM opportunity data...")
        extractor = CRMDataExtractor()
        crm_data = extractor.extract(documents)

        # Print the extracted data
        print("\nExtracted CRM Opportunity Data:")
        print(json.dumps(crm_data.model_dump(), indent=2))

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
