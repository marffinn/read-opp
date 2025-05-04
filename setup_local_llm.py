#!/usr/bin/env python3
"""
Setup script for the local LLM version of the PDF CRM Extractor.

This script:
1. Installs the required packages
2. Downloads the Mistral 7B model
"""

import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Install the required packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {str(e)}")
        sys.exit(1)

def download_model():
    """Download the Mistral 7B model."""
    print("Downloading Mistral 7B model...")
    try:
        # Run the download_model.py script
        subprocess.check_call([sys.executable, "download_model.py"])
    except subprocess.CalledProcessError as e:
        print(f"Error downloading model: {str(e)}")
        sys.exit(1)

def main():
    """Run the setup process."""
    print("Setting up the local LLM version of the PDF CRM Extractor...")
    
    # Install requirements
    install_requirements()
    
    # Download model
    download_model()
    
    print("\nSetup complete!")
    print("You can now run the PDF CRM Extractor with the local LLM.")
    print("To extract data from a PDF, run:")
    print("python src/main.py extract path/to/your/document.pdf")

if __name__ == "__main__":
    main()
