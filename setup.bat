@echo off
echo Setting up PDF CRM Extractor...

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Create .env file from example if it doesn't exist
if not exist .env (
    copy .env.example .env
    echo Created .env file from template. Please edit it to add your API keys.
)

echo.
echo Setup complete! You can now use the PDF CRM Extractor.
echo To get started, try creating a test PDF:
echo python examples/create_test_pdf.py
echo.
echo Then extract data from it:
echo python src/main.py extract test_opportunity.pdf
