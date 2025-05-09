# Text-Based CRM Opportunity Extractor

A lightweight web application that uses a local LLM (Large Language Model) to extract structured CRM opportunity data from text. This tool helps sales and business development teams quickly process opportunity information without relying on external APIs.

## Features

- **Text Input**: Paste text from opportunity documents, emails, or any source
- **Local LLM Processing**: Uses Mistral 7B for local processing without sending data to external services
- **Structured Data Extraction**: Extracts key CRM fields like company name, contact details, project requirements, etc.
- **Export Options**: Export extracted data as JSON or CSV
- **Logging**: Comprehensive logging for troubleshooting

## Installation

### Prerequisites

- Python 3.8 or higher
- Git (optional, only needed if cloning the repository)

### One-Click Installation (Windows)

1. Download or clone this repository to your local machine.

2. Double-click on `INSTALL.bat` to run the comprehensive installation script.
   - This will automatically run PowerShell with the correct permissions
   - No manual PowerShell commands needed

3. The installation script will:
   - Create a virtual environment
   - Install all dependencies
   - Create necessary directories
   - Set up environment files
   - Download the Mistral 7B model (about 4.1GB)
   - Install model support libraries
   - Create a startup batch file

4. Once installation is complete, you can start the application by double-clicking `start_app.bat`.

> **Note**: The Mistral model is large (about 4.1GB) and may take some time to download depending on your internet connection. The installation will continue in the background if you don't want to wait.

### Manual Setup

If you prefer to set up manually or are using a non-Windows system:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/crm-opportunity-extractor.git
   cd crm-opportunity-extractor
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up environment variables (optional):
   ```
   cp .env.example .env
   ```

   Edit the `.env` file if you want to use OpenAI or other API-based models.

6. Download the Mistral 7B model (optional):
   ```
   mkdir -p models
   # Download the model file to the models directory
   # You can use wget, curl, or manually download
   # Example:
   # wget -O models/mistral-7b-instruct-v0.2.Q4_K_M.gguf https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf
   ```

   Note: If you don't have the model, the application will fall back to a rule-based extraction method.

## Usage

### Windows Quick Start

1. Double-click `start_app.bat` to launch the application.

2. Your default web browser should open automatically to http://127.0.0.1:5000/
   - If it doesn't open, manually navigate to this address in your browser.

3. Paste text from your opportunity document into the text area.

4. Click "Extract Data" to process the text.

5. View the extracted CRM data in the results section.

6. Optionally export the data as JSON or CSV.

7. To stop the application, go back to the command window and press Ctrl+C.

### Manual Start

If you prefer to start the application manually:

1. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

2. Start the application:
   ```
   python simple_app.py
   ```

3. Open your web browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

4. Follow steps 3-6 from the Quick Start section above.

## Example Input

The application works best with text that contains structured information about business opportunities. For example:

```
Zapytanie ofertowe nr: 12345678 Ważne do: 2025-06-30 23:59
Zlecenia na wykonanie sklepu internetowego, Warszawa
Mazowieckie, powiat warszawski, 00-001, Warszawa
Usługi dla firmy, biura >> Marketing internetowy >> Sklepy internetowe

Zakres zlecenia: wykonanie sklepu
Branża sklepu: ELEKTRONIKA
Projekt graficzny: Klient nie ma projektu, ale wie czego oczekuje
Orientacyjna liczba produktów: 100-500
Integracje: płatności, portale sprzedażowe, firmy kurierskie, programy księgowe
Inne potrzeby Klienta: migracja sklepu
Termin realizacji usługi: do końca kwartału

Kontakt do Jan Kowalski
e-mail: jan.kowalski@example.com
tel: +48123456789

Firma: Example Electronics
powiat warszawski
```

## AI Model Information

The application uses a local LLM (Mistral 7B) for extraction without requiring an API key or internet connection. If the model is not available, it will fall back to a rule-based extraction method that uses regular expressions to identify common patterns in the text.

### Model Setup

1. Download the Mistral 7B model from Hugging Face:
   ```
   https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf
   ```

2. Place the model file in the `models` directory.

3. Install the ctransformers package:
   ```
   pip install ctransformers
   ```

### Using API-Based Models (Optional)

By default, the application uses the local Mistral 7B model or falls back to rule-based extraction. If you prefer to use OpenAI or other API-based models:

1. Copy the example environment file:
   ```
   cp .env.example .env
   ```

2. Edit the `.env` file and add your API keys:
   ```
   # OpenAI API Key
   OPENAI_API_KEY=your_openai_api_key_here

   # Hugging Face API Token
   HUGGINGFACE_API_TOKEN=your_huggingface_token_here
   ```

3. The application will automatically detect and use the API-based models if the keys are present.

> **Security Note**: Never commit your `.env` file with actual API keys to version control. The `.env` file is included in `.gitignore` to prevent accidental commits.

## Extracted Fields

The application extracts the following fields:

- Company Name
- Contact Name
- Contact Email
- Contact Phone
- Location
- Project Type
- Industry
- Product Count
- Design Requirements
- Integration Requirements
- Other Requirements
- Opportunity Value
- Timeline
- Products/Services
- Opportunity Stage
- Probability
- Notes

## Customization

### Adding New Extraction Patterns

To add new extraction patterns, edit the `src/crm_extractor/extractor.py` file. Look for the pattern definitions in the `extract` method and add your own regular expressions.

### Modifying the Data Model

To add or modify the fields in the data model, edit the `CRMOpportunity` class in `src/crm_extractor/extractor.py`.

## Troubleshooting

### Model Loading Issues

If you see an error like:
```
Error loading local model: Could not import `ctransformers` package. Please install it with `pip install ctransformers`
```

Install the required package:
```
pip install ctransformers
```

### Other Issues

Check the logs in the `logs` directory for detailed error information.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Mistral AI](https://mistral.ai/) for the Mistral 7B model
- [LangChain](https://www.langchain.com/) for the document processing framework
- [Flask](https://flask.palletsprojects.com/) for the web framework
