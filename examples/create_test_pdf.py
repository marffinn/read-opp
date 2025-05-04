#!/usr/bin/env python3
"""
Script to create a sample PDF file for testing the CRM extractor.
"""

import sys
from fpdf import FPDF

def create_test_pdf(output_path="test_opportunity.pdf"):
    """Create a sample PDF with CRM opportunity information."""
    pdf = FPDF()
    pdf.add_page()
    
    # Set font
    pdf.set_font("Arial", size=12)
    
    # Add content
    pdf.cell(200, 10, txt="SALES OPPORTUNITY REPORT", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt="Company Information:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Company Name: Acme Corporation", ln=True)
    pdf.cell(200, 10, txt="Industry: Technology", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt="Contact Information:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Contact Name: John Smith", ln=True)
    pdf.cell(200, 10, txt="Position: Chief Technology Officer", ln=True)
    pdf.cell(200, 10, txt="Email: john.smith@acmecorp.com", ln=True)
    pdf.cell(200, 10, txt="Phone: (555) 123-4567", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt="Opportunity Details:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Opportunity Value: $75,000 USD", ln=True)
    pdf.cell(200, 10, txt="Products of Interest: Cloud Storage, Data Analytics", ln=True)
    pdf.cell(200, 10, txt="Timeline: Q3 2023", ln=True)
    pdf.cell(200, 10, txt="Opportunity Stage: Proposal", ln=True)
    pdf.cell(200, 10, txt="Probability: 65%", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt="Notes:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Acme Corporation is looking to upgrade their data storage and analytics capabilities. They are currently evaluating our solution against two competitors. The CTO has expressed particular interest in our real-time analytics features. A follow-up meeting is scheduled for next month.")
    
    # Save the PDF
    pdf.output(output_path)
    print(f"Created test PDF at: {output_path}")

if __name__ == "__main__":
    output_path = "test_opportunity.pdf"
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    create_test_pdf(output_path)
