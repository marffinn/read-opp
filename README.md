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
- Git

### Setup

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

5. Download the Mistral 7B model:
   ```
   mkdir -p models
   # Download the model file to the models directory
   # You can use wget, curl, or manually download
   # Example:
   # wget -O models/mistral-7b-instruct-v0.2.Q4_K_M.gguf https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf
   ```

   Note: If you don't have the model, the application will fall back to a rule-based extraction method.

## Usage

1. Start the application:
   ```
   python simple_app.py
   ```

2. Open your web browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

3. Paste text from your opportunity document into the text area.

4. Click "Extract Data" to process the text.

5. View the extracted CRM data in the results section.

6. Optionally export the data as JSON or CSV.

## Example Input

The application works best with text that contains structured information about business opportunities. For example:

```
Zapytanie ofertowe nr: 15700829 Ważne do: 2025-04-12 23:59
Zlecenia na wykonanie sklepu internetowego, Wyry
Śląskie, powiat mikołowski, 43-175, Wyry
Usługi dla firmy, biura >> Marketing internetowy >> Sklepy internetowe

Zakres zlecenia: wykonanie sklepu
Branża sklepu: PUCHARY
Projekt graficzny: Klient nie ma projektu, ale wie czego oczekuje
Orientacyjna liczba produktów: 501-1000
Integracje: płatności, portale sprzedażowe/porównywarkI, firmy kurierskie, hurtownie, programy księgowe/magazynowe
Inne potrzeby Klienta: migracja sklepu
Termin realizacji usługi: możliwe od zaraz

Kontakt do Jarosław Góralczyk
e-mail: info@twojetrofeum.pl
tel: +48602395561

Firma: Trofeum
powiat mikołowski
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
