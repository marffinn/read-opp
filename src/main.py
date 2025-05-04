#!/usr/bin/env python3
"""
PDF CRM Opportunity Extractor

This tool extracts CRM opportunity data from PDF documents using AI.
"""

import os
import sys
import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
import click
from dotenv import load_dotenv

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from pdf_processor.loader import PDFLoader
from crm_extractor.extractor import CRMDataExtractor
from interface.output_formatter import format_as_json, format_as_csv

# Load environment variables
load_dotenv()

@click.group()
def cli():
    """Extract CRM opportunity data from PDF documents using AI."""
    pass

@cli.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--output-format', '-f', type=click.Choice(['json', 'csv']), default='json',
              help='Output format for the extracted data')
@click.option('--output-file', '-o', type=click.Path(), help='Output file path')
def extract(pdf_path: str, output_format: str, output_file: Optional[str]):
    """Extract CRM opportunity data from a single PDF file."""
    try:
        # Load the PDF
        loader = PDFLoader()
        document = loader.load(pdf_path)

        # Extract CRM data
        extractor = CRMDataExtractor()
        crm_data = extractor.extract(document)

        # Format and output the data
        if output_format == 'json':
            formatted_data = format_as_json(crm_data)
            if output_file:
                with open(output_file, 'w') as f:
                    f.write(formatted_data)
            else:
                click.echo(formatted_data)
        else:  # csv
            formatted_data = format_as_csv(crm_data)
            if output_file:
                with open(output_file, 'w', newline='') as f:
                    f.write(formatted_data)
            else:
                click.echo(formatted_data)

        click.echo(f"Successfully extracted CRM data from {pdf_path}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--output-format', '-f', type=click.Choice(['json', 'csv']), default='json',
              help='Output format for the extracted data')
@click.option('--output-dir', '-o', type=click.Path(), help='Output directory path')
def batch(directory: str, output_format: str, output_dir: Optional[str]):
    """Process multiple PDF files in a directory."""
    try:
        # Create output directory if it doesn't exist
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Get all PDF files in the directory
        pdf_files = list(Path(directory).glob('*.pdf'))
        if not pdf_files:
            click.echo("No PDF files found in the specified directory.")
            return

        click.echo(f"Found {len(pdf_files)} PDF files to process.")

        # Process each PDF file
        for pdf_file in pdf_files:
            click.echo(f"Processing {pdf_file}...")

            # Determine output file path
            if output_dir:
                output_file = os.path.join(output_dir, f"{pdf_file.stem}.{output_format}")
            else:
                output_file = None

            # Load the PDF
            loader = PDFLoader()
            document = loader.load(str(pdf_file))

            # Extract CRM data
            extractor = CRMDataExtractor()
            crm_data = extractor.extract(document)

            # Format and output the data
            if output_format == 'json':
                formatted_data = format_as_json(crm_data)
                if output_file:
                    with open(output_file, 'w') as f:
                        f.write(formatted_data)
                else:
                    click.echo(formatted_data)
            else:  # csv
                formatted_data = format_as_csv(crm_data)
                if output_file:
                    with open(output_file, 'w', newline='') as f:
                        f.write(formatted_data)
                else:
                    click.echo(formatted_data)

            click.echo(f"Successfully extracted CRM data from {pdf_file}")

        click.echo("Batch processing complete.")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
