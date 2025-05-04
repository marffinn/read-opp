#!/bin/bash

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from template. Please edit it to add your API keys."
fi

echo "Setup complete! You can now use the PDF CRM Extractor."
echo "To get started, try creating a test PDF:"
echo "python examples/create_test_pdf.py"
echo ""
echo "Then extract data from it:"
echo "python src/main.py extract test_opportunity.pdf"
