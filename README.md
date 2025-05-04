# Text-Based CRM Opportunity Extractor

A lightweight web application that uses a local LLM (Large Language Model) to extract structured CRM opportunity data from text. This tool helps sales and business development teams quickly process opportunity information without relying on external APIs.

## Features

- **Text Input**: Paste text from opportunity documents, emails, or any source
- **Local LLM Processing**: Uses Mistral 7B for local processing without sending data to external services
- **Structured Data Extraction**: Extracts key CRM fields like company name, contact details, project requirements, etc.
- **Export Options**: Export extracted data as JSON or CSV
- **Logging**: Comprehensive logging for troubleshooting

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/pdf-crm-extractor.git
   cd pdf-crm-extractor
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your API keys:
   ```
   cp .env.example .env
   ```
   Then edit the `.env` file to add your API keys.

## Usage

### Extract data from a single PDF

```bash
python src/main.py extract path/to/your/document.pdf
```

Options:
- `--output-format` or `-f`: Output format (`json` or `csv`), default is `json`
- `--output-file` or `-o`: Save output to a file instead of printing to console

Example:
```bash
python src/main.py extract sales_proposal.pdf --output-format csv --output-file opportunity.csv
```

### Batch process multiple PDFs

```bash
python src/main.py batch path/to/pdf/directory
```

Options:
- `--output-format` or `-f`: Output format (`json` or `csv`), default is `json`
- `--output-dir` or `-o`: Directory to save output files

Example:
```bash
python src/main.py batch sales_documents/ --output-format json --output-dir extracted_data/
```

## AI Model Options

The tool supports multiple AI model options:

### Local LLM (Recommended)

The tool can use a local LLM (Mistral 7B) for extraction without requiring an API key or internet connection:

1. Run the setup script to install dependencies and download the model:
   ```
   python setup_local_llm.py
   ```

2. The model will be downloaded to the `models` directory and automatically used by the extractor.

### OpenAI API

Alternatively, you can use OpenAI's GPT-3.5 Turbo model by setting your API key in the `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

### Other Options

You can configure different models by setting the appropriate environment variables in the `.env` file:

- For Hugging Face: Set `HUGGINGFACE_API_TOKEN`
- For custom local models: Set `LOCAL_MODEL_PATH` to point to your model file

## CRM Data Schema

The tool extracts the following information:

- Company name
- Contact name
- Contact email and phone
- Opportunity value and currency
- Timeline
- Products/services of interest
- Opportunity stage
- Probability of closing
- Additional notes

## License

MIT
