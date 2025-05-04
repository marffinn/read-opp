"""
PDF Loader Module

This module handles loading and parsing PDF documents.
"""

import os
from typing import Dict, List, Any
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

class PDFLoader:
    """Class for loading and parsing PDF documents."""

    def __init__(self):
        """Initialize the PDF loader."""
        pass

    def load(self, pdf_path: str) -> List[Document]:
        """
        Load a PDF file and convert it to a list of Document objects.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            List of Document objects containing the text content
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            return documents
        except Exception as e:
            raise Exception(f"Error loading PDF: {str(e)}")

    def get_metadata(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract metadata from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary containing PDF metadata
        """
        # This is a placeholder for PDF metadata extraction
        # In a real implementation, you would use a library like PyPDF2 or pikepdf
        # to extract detailed metadata
        return {
            "filename": os.path.basename(pdf_path),
            "path": pdf_path,
            "size_bytes": os.path.getsize(pdf_path),
            "last_modified": os.path.getmtime(pdf_path)
        }
