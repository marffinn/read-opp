#!/usr/bin/env python3
"""
Simple web interface for the Text-Based CRM Opportunity Extractor.
"""

import os
import json
import logging
import datetime
from flask import Flask, render_template_string, request, redirect, url_for, flash, session

# Set up logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f"extraction_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import our CRM extractor modules
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.crm_extractor.extractor import CRMDataExtractor

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages and session

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Text-Based CRM Opportunity Extractor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #2c3e50;
        }
        .container {
            background-color: #f9f9f9;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="file"] {
            display: block;
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #2980b9;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
            width: 30%;
        }
        .flash {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        .flash.success {
            background-color: #d4edda;
            color: #155724;
        }
        .flash.error {
            background-color: #f8d7da;
            color: #721c24;
        }
        .text-input-container {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Text-Based CRM Opportunity Extractor</h1>

    {% if messages %}
        {% for category, message in messages %}
            <div class="flash {{ category }}">{{ message }}</div>
        {% endfor %}
    {% endif %}

    {% if results %}
        <div class="container">
            <h2>Extraction Results</h2>
            <p>CRM opportunity data extracted from <strong>{{ filename }}</strong></p>

            <table>
                <tr>
                    <th>Company Name</th>
                    <td>{{ results.company_name }}</td>
                </tr>
                <tr>
                    <th>Contact Name</th>
                    <td>{{ results.contact_name or 'N/A' }}</td>
                </tr>
                <tr>
                    <th>Contact Email</th>
                    <td>{{ results.contact_email or 'N/A' }}</td>
                </tr>
                <tr>
                    <th>Contact Phone</th>
                    <td>{{ results.contact_phone or 'N/A' }}</td>
                </tr>
                <tr>
                    <th>Location</th>
                    <td>{{ results.location or 'N/A' }}</td>
                </tr>
                <tr>
                    <th>Project Type</th>
                    <td>{{ results.project_type or 'N/A' }}</td>
                </tr>
                <tr>
                    <th>Industry</th>
                    <td>{{ results.industry or 'N/A' }}</td>
                </tr>
                <tr>
                    <th>Product Count</th>
                    <td>{{ results.product_count or 'N/A' }}</td>
                </tr>
                <tr>
                    <th>Design Requirements</th>
                    <td>{{ results.design_requirements or 'N/A' }}</td>
                </tr>
                <tr>
                    <th>Integration Requirements</th>
                    <td>
                        {% if results.integration_requirements %}
                            <ul>
                                {% for item in results.integration_requirements %}
                                    <li>{{ item }}</li>
                                {% endfor %}
                            </ul>
                        {% else %}
                            N/A
                        {% endif %}
                    </td>
                </tr>
                <tr>
                    <th>Other Requirements</th>
                    <td>
                        {% if results.other_requirements %}
                            <ul>
                                {% for item in results.other_requirements %}
                                    <li>{{ item }}</li>
                                {% endfor %}
                            </ul>
                        {% else %}
                            N/A
                        {% endif %}
                    </td>
                </tr>
                <tr>
                    <th>Opportunity Value</th>
                    <td>
                        {% if results.opportunity_value %}
                            {{ results.opportunity_value }} {{ results.currency or '' }}
                        {% else %}
                            N/A
                        {% endif %}
                    </td>
                </tr>
                <tr>
                    <th>Timeline</th>
                    <td>{{ results.timeline or 'N/A' }}</td>
                </tr>
                <tr>
                    <th>Products/Services</th>
                    <td>
                        {% if results.product_interest %}
                            <ul>
                                {% for product in results.product_interest %}
                                    <li>{{ product }}</li>
                                {% endfor %}
                            </ul>
                        {% else %}
                            N/A
                        {% endif %}
                    </td>
                </tr>
                <tr>
                    <th>Opportunity Stage</th>
                    <td>{{ results.opportunity_stage or 'N/A' }}</td>
                </tr>
                <tr>
                    <th>Probability</th>
                    <td>
                        {% if results.probability %}
                            {{ results.probability }}%
                        {% else %}
                            N/A
                        {% endif %}
                    </td>
                </tr>
                <tr>
                    <th>Notes</th>
                    <td>{{ results.notes or 'N/A' }}</td>
                </tr>
            </table>

            <div style="margin-top: 20px;">
                <button onclick="exportJSON()">Export as JSON</button>
                <button onclick="exportCSV()">Export as CSV</button>
            </div>

            <script>
                function exportJSON() {
                    const data = {{ results|tojson }};
                    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = '{{ filename }}'.replace('.pdf', '') + '_crm_data.json';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                }

                function exportCSV() {
                    const data = {{ results|tojson }};
                    let csv = 'Field,Value\\n';

                    for (const [key, value] of Object.entries(data)) {
                        if (key === 'product_interest' && Array.isArray(value)) {
                            csv += `${key},"${value.join(', ')}"\\n`;
                        } else {
                            csv += `${key},"${value}"\\n`;
                        }
                    }

                    const blob = new Blob([csv], { type: 'text/csv' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = '{{ filename }}'.replace('.pdf', '') + '_crm_data.csv';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                }
            </script>
        </div>
    {% endif %}

    <div class="container">
        <h2>Extract CRM Data</h2>
        <p>Paste text from your opportunity documents to extract CRM data using a local LLM.</p>

        <div class="text-input-container">
            <h3>Paste Text</h3>
            <p>Copy and paste text content from your document</p>
            <form action="{{ url_for('extract_text') }}" method="post">
                <div class="form-group">
                    <label for="pdf_text">Text content:</label>
                    <textarea id="pdf_text" name="pdf_text" rows="12" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;" required></textarea>
                </div>
                <button type="submit">Extract Data</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Render the home page with the upload form."""
    messages = []
    results = None
    filename = None

    # Check if there are flash messages
    flashed_messages = session.pop('_flashes', [])
    for category, message in flashed_messages:
        messages.append((category, message))

    # Check if there are extraction results
    if 'extraction_results' in session:
        results = session['extraction_results']
        filename = session.get('filename', 'Unknown file')

    return render_template_string(
        HTML_TEMPLATE,
        messages=messages,
        results=results,
        filename=filename
    )

# Route removed - we now only use text input

@app.route('/extract-text', methods=['POST'])
def extract_text():
    """Handle text input extraction."""
    logging.info("Text extraction request received")

    # Get the text from the form
    text_content = request.form.get('pdf_text', '')

    if not text_content.strip():
        logging.warning("No text content provided")
        flash('No text content provided', 'error')
        return redirect(url_for('index'))

    try:
        # Create a document from the text
        from langchain_core.documents import Document
        document = Document(page_content=text_content)

        # Log the first 500 characters of the text content
        logging.info(f"Text content preview: {text_content[:500]}...")

        # Extract CRM data
        logging.info("Extracting CRM data from text")
        extractor = CRMDataExtractor()
        crm_data = extractor.extract([document])

        # Log the extracted data
        logging.info(f"Extracted data: {crm_data.model_dump()}")

        # Store the results in the session
        session['extraction_results'] = crm_data.model_dump()
        session['filename'] = "Text Input"

        # Also save the results to a JSON file
        results_dir = "extraction_results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = os.path.join(results_dir, f"text_input_{timestamp}_results.json")
        with open(results_file, 'w') as f:
            json.dump(crm_data.model_dump(), f, indent=2)
        logging.info(f"Results saved to {results_file}")

        flash('Text processed successfully!', 'success')

    except Exception as e:
        logging.error(f"Error processing text: {str(e)}", exc_info=True)
        flash(f'Error processing text: {str(e)}', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    print("Starting Text-Based CRM Opportunity Extractor web interface...")
    print("Open your browser and go to http://127.0.0.1:5000/")
    print(f"Logs will be saved to: {log_file}")
    print(f"Extraction results will be saved to the 'extraction_results' directory")

    # Log system information
    logging.info("=== Text-Based CRM Opportunity Extractor Web Interface Starting ===")
    logging.info(f"Current working directory: {os.getcwd()}")

    # Check if the model exists
    model_path = os.path.join("models", "mistral-7b-instruct-v0.2.Q4_K_M.gguf")
    if os.path.exists(model_path):
        logging.info(f"Local LLM found at: {os.path.abspath(model_path)}")
    else:
        logging.warning(f"Local LLM not found at: {os.path.abspath(model_path)}")

    app.run(debug=True)
