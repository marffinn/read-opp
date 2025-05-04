"""
CRM Data Extractor Module

This module extracts structured CRM opportunity data from document text using AI.
"""

import os
import sys
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.documents import Document
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms import CTransformers
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Define CRM Opportunity data model
class CRMOpportunity(BaseModel):
    """Data model for CRM opportunity information."""

    company_name: str = Field(description="Name of the company")
    contact_name: Optional[str] = Field(None, description="Primary contact name")
    contact_email: Optional[str] = Field(None, description="Contact email address")
    contact_phone: Optional[str] = Field(None, description="Contact phone number")
    opportunity_value: Optional[float] = Field(None, description="Monetary value of the opportunity")
    currency: Optional[str] = Field(None, description="Currency of the opportunity value")
    timeline: Optional[str] = Field(None, description="Expected timeline or deadline")
    product_interest: Optional[List[str]] = Field(None, description="Products or services of interest")
    opportunity_stage: Optional[str] = Field(None, description="Current stage in the sales process")
    probability: Optional[float] = Field(None, description="Probability of closing (0-100%)")
    notes: Optional[str] = Field(None, description="Additional notes or context")

    # Additional fields for more detailed opportunity information
    location: Optional[str] = Field(None, description="Location or address")
    project_type: Optional[str] = Field(None, description="Type of project")
    industry: Optional[str] = Field(None, description="Industry or business category")
    product_count: Optional[str] = Field(None, description="Number of products")
    design_requirements: Optional[str] = Field(None, description="Design requirements")
    integration_requirements: Optional[List[str]] = Field(None, description="Integration requirements")
    other_requirements: Optional[List[str]] = Field(None, description="Other client requirements")

class CRMDataExtractor:
    """Class for extracting CRM data from documents using AI."""

    def __init__(self):
        """
        Initialize the CRM data extractor.
        """
        # Check for local model first
        model_path = os.path.join("models", "mistral-7b-instruct-v0.2.Q4_K_M.gguf")
        local_model_path = os.getenv("LOCAL_MODEL_PATH", model_path)

        print(f"Looking for model at: {os.path.abspath(local_model_path)}")

        # Try to use local LLM if available
        if os.path.exists(local_model_path):
            try:
                print(f"Using local LLM: {local_model_path}")
                # Get absolute path to model
                abs_model_path = os.path.abspath(local_model_path)
                print(f"Absolute model path: {abs_model_path}")

                self.llm = CTransformers(
                    model=abs_model_path,
                    model_type="mistral",
                    config={
                        'max_new_tokens': 1024,
                        'temperature': 0.1,
                        'context_length': 2048,
                    }
                )
                print("Successfully loaded the model!")
            except Exception as e:
                print(f"Error loading local model: {str(e)}")
                print("Falling back to dummy extractor.")
                self.llm = None
        # Fallback to OpenAI if local model not available and API key exists
        elif os.getenv("OPENAI_API_KEY"):
            try:
                self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
                print(f"Using OpenAI model: gpt-3.5-turbo")
            except Exception as e:
                print(f"Error initializing OpenAI: {str(e)}")
                print("Falling back to dummy extractor.")
                self.llm = None
        else:
            print("No local model or API key found. Using dummy extractor.")
            self.llm = None

        # Create the prompt template for CRM data extraction
        self.prompt_template = PromptTemplate(
            input_variables=["document_text"],
            template="""
            You are an AI assistant specialized in extracting CRM opportunity data from documents.

            Please analyze the following document text and extract structured information about potential sales opportunities.

            Document text:
            {document_text}

            Extract the following information in JSON format:
            - company_name: The name of the company mentioned
            - contact_name: The name of the primary contact person
            - contact_email: Email address of the contact
            - contact_phone: Phone number of the contact
            - opportunity_value: The monetary value of the opportunity (just the number)
            - currency: The currency of the opportunity value
            - timeline: Expected timeline or deadline for the opportunity
            - product_interest: List of products or services the company is interested in
            - opportunity_stage: Current stage in the sales process
            - probability: Probability of closing the deal (0-100%)
            - notes: Any additional relevant information

            If any field is not found in the document, set it to null.
            Return ONLY the JSON object, nothing else.
            """
        )

        # Create the LLM chain
        if self.llm:
            self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def extract(self, documents: List[Document]) -> CRMOpportunity:
        """
        Extract CRM opportunity data from documents.

        Args:
            documents: List of Document objects containing text

        Returns:
            CRMOpportunity object with extracted data
        """
        # Combine all document texts
        combined_text = "\n\n".join([doc.page_content for doc in documents])

        if not self.llm:
            # Simple rule-based extraction for the dummy implementation
            try:
                print("Using rule-based extraction as fallback")
                print(f"Document text length: {len(combined_text)} characters")
                print(f"First 200 characters: {combined_text[:200]}...")

                # Try to extract some basic information from the text
                company_name = "Unknown Company"
                contact_name = None
                contact_email = None
                contact_phone = None
                opportunity_value = None
                currency = None
                timeline = None
                product_interest = []
                opportunity_stage = None
                probability = None
                notes = None

                import re

                # Look for patterns in the text - including Polish language patterns
                # Company name patterns
                company_patterns = [
                    r"Company Name:\s*(.*?)(?:\n|$)",
                    r"Company:\s*(.*?)(?:\n|$)",
                    r"Organization:\s*(.*?)(?:\n|$)",
                    r"Client:\s*(.*?)(?:\n|$)",
                    r"Firma:\s*(.*?)(?:\n|$)",
                    r"Nazwa firmy:\s*(.*?)(?:\n|$)",
                    r"Klient:\s*(.*?)(?:\n|$)"
                ]

                for pattern in company_patterns:
                    match = re.search(pattern, combined_text, re.IGNORECASE)
                    if match:
                        company_name = match.group(1).strip()
                        break

                # Also look for specific Polish format in the text
                firma_match = re.search(r"Firma:\s*(.*?)(?:\n|$)", combined_text)
                if firma_match:
                    company_name = firma_match.group(1).strip()

                # Contact name patterns
                contact_patterns = [
                    r"Contact Name:\s*(.*?)(?:\n|$)",
                    r"Contact:\s*(.*?)(?:\n|$)",
                    r"Name:\s*(.*?)(?:\n|$)",
                    r"Person:\s*(.*?)(?:\n|$)",
                    r"Kontakt do\s*(.*?)(?:\n|$)",
                    r"Osoba kontaktowa:\s*(.*?)(?:\n|$)",
                    r"Kontakt:\s*(.*?)(?:\n|$)"
                ]

                for pattern in contact_patterns:
                    match = re.search(pattern, combined_text, re.IGNORECASE)
                    if match:
                        contact_name = match.group(1).strip()
                        break

                # Email patterns
                email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", combined_text)
                if email_match:
                    contact_email = email_match.group(0)

                # Also look for e-mail: prefix
                email_prefix_match = re.search(r"e-mail:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", combined_text, re.IGNORECASE)
                if email_prefix_match:
                    contact_email = email_prefix_match.group(1).strip()

                # Phone patterns
                phone_patterns = [
                    r"Phone:\s*([\d\s\(\)\+\-\.]+)(?:\n|$)",
                    r"Tel(?:ephone)?:\s*([\d\s\(\)\+\-\.]+)(?:\n|$)",
                    r"Contact(?:\s+Number)?:\s*([\d\s\(\)\+\-\.]+)(?:\n|$)",
                    r"tel:\s*([\d\s\(\)\+\-\.]+)(?:\n|$)",
                    r"telefon:\s*([\d\s\(\)\+\-\.]+)(?:\n|$)",
                    r"(?<!\w)(?:\+\d{1,3}[\s\-\.]?)?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}(?!\d)",
                    r"(?<!\w)(?:\+\d{1,2})?[\s\-\.]?\d{3}[\s\-\.]?\d{3}[\s\-\.]?\d{3}(?!\d)"  # Polish format
                ]

                for pattern in phone_patterns:
                    match = re.search(pattern, combined_text, re.IGNORECASE)
                    if match:
                        contact_phone = match.group(1).strip() if len(match.groups()) > 0 else match.group(0).strip()
                        break

                # Location patterns (for Polish addresses)
                location_patterns = [
                    r"(?:Śląskie|Małopolskie|Mazowieckie|Dolnośląskie|Wielkopolskie|Łódzkie|Pomorskie|Podkarpackie|Lubelskie|Podlaskie|Kujawsko-Pomorskie|Zachodniopomorskie|Warmińsko-Mazurskie|Opolskie|Lubuskie|Świętokrzyskie),\s*(?:powiat|pow\.|p\.)\s*([a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s-]+),\s*(\d{2}-\d{3}),\s*([a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s-]+)"
                ]

                for pattern in location_patterns:
                    match = re.search(pattern, combined_text)
                    if match:
                        location = match.group(0).strip()
                        break

                # Project type patterns
                project_patterns = [
                    r"Zakres zlecenia:\s*(.*?)(?:\n|$)",
                    r"Projekt:\s*(.*?)(?:\n|$)",
                    r"Zlecenie na\s*(.*?)(?:\n|$)",
                    r"wykonanie\s*(.*?)(?:\n|$)"
                ]

                for pattern in project_patterns:
                    match = re.search(pattern, combined_text, re.IGNORECASE)
                    if match:
                        project_type = match.group(1).strip()
                        break

                # Industry patterns
                industry_patterns = [
                    r"Branża(?:\s+sklepu)?:\s*(.*?)(?:\n|$)",
                    r"Industry:\s*(.*?)(?:\n|$)",
                    r"Sector:\s*(.*?)(?:\n|$)"
                ]

                for pattern in industry_patterns:
                    match = re.search(pattern, combined_text, re.IGNORECASE)
                    if match:
                        industry = match.group(1).strip()
                        break

                # Product count patterns
                product_count_patterns = [
                    r"(?:Orientacyjna\s+)?[Ll]iczba\s+produktów:\s*(.*?)(?:\n|$)",
                    r"Number of products:\s*(.*?)(?:\n|$)",
                    r"Products count:\s*(.*?)(?:\n|$)"
                ]

                for pattern in product_count_patterns:
                    match = re.search(pattern, combined_text, re.IGNORECASE)
                    if match:
                        product_count = match.group(1).strip()
                        break

                # Design requirements patterns
                design_patterns = [
                    r"Projekt graficzny:\s*(.*?)(?:\n|$)",
                    r"Design:\s*(.*?)(?:\n|$)",
                    r"Graphics:\s*(.*?)(?:\n|$)"
                ]

                for pattern in design_patterns:
                    match = re.search(pattern, combined_text, re.IGNORECASE)
                    if match:
                        design_requirements = match.group(1).strip()
                        break

                # Integration requirements patterns
                integration_patterns = [
                    r"Integracje:\s*(.*?)(?:\n\n|\n[A-Z]|$)",
                    r"Integrations:\s*(.*?)(?:\n\n|\n[A-Z]|$)"
                ]

                integration_requirements = []
                for pattern in integration_patterns:
                    match = re.search(pattern, combined_text, re.IGNORECASE | re.DOTALL)
                    if match:
                        integrations_text = match.group(1).strip()
                        # Try to split by commas or new lines
                        if ',' in integrations_text:
                            integration_requirements = [p.strip() for p in integrations_text.split(',')]
                        else:
                            integration_requirements = [p.strip() for p in integrations_text.split('\n') if p.strip()]
                        break

                # Other requirements patterns
                other_req_patterns = [
                    r"Inne potrzeby Klienta:\s*(.*?)(?:\n\n|\n[A-Z]|$)",
                    r"Other requirements:\s*(.*?)(?:\n\n|\n[A-Z]|$)"
                ]

                other_requirements = []
                for pattern in other_req_patterns:
                    match = re.search(pattern, combined_text, re.IGNORECASE | re.DOTALL)
                    if match:
                        reqs_text = match.group(1).strip()
                        # Try to split by commas or new lines
                        if ',' in reqs_text:
                            other_requirements = [p.strip() for p in reqs_text.split(',')]
                        else:
                            other_requirements = [p.strip() for p in reqs_text.split('\n') if p.strip()]
                        break

                # Timeline patterns
                timeline_patterns = [
                    r"Timeline:?\s*(.*?)(?:\n|$)",
                    r"Deadline:?\s*(.*?)(?:\n|$)",
                    r"Time frame:?\s*(.*?)(?:\n|$)",
                    r"Schedule:?\s*(.*?)(?:\n|$)",
                    r"Termin realizacji(?:\s+usługi)?:\s*(.*?)(?:\n|$)",
                    r"(?:Q[1-4]|Quarter [1-4])[\s\-]?20\d\d"
                ]

                for pattern in timeline_patterns:
                    match = re.search(pattern, combined_text, re.IGNORECASE)
                    if match:
                        timeline = match.group(1).strip() if len(match.groups()) > 0 else match.group(0).strip()
                        break

                # Notes patterns
                notes_patterns = [
                    r"Notes:?\s*(.*?)(?=\n\n|\Z)",
                    r"Comments:?\s*(.*?)(?=\n\n|\Z)",
                    r"Additional Information:?\s*(.*?)(?=\n\n|\Z)",
                    r"Description:?\s*(.*?)(?=\n\n|\Z)",
                    r"Details:?\s*(.*?)(?=\n\n|\Z)"
                ]

                for pattern in notes_patterns:
                    match = re.search(pattern, combined_text, re.IGNORECASE | re.DOTALL)
                    if match:
                        notes = match.group(1).strip()
                        break

                # If we still don't have notes, try to extract the last paragraph
                if not notes and len(combined_text.strip()) > 0:
                    paragraphs = [p for p in combined_text.split('\n\n') if p.strip()]
                    if paragraphs and len(paragraphs) > 3:  # Only use last paragraph if we have several
                        notes = paragraphs[-1].strip()

                # Print what we extracted
                print(f"Extracted data from rule-based approach:")
                print(f"  Company: {company_name}")
                print(f"  Contact: {contact_name}")
                print(f"  Email: {contact_email}")
                print(f"  Phone: {contact_phone}")
                print(f"  Value: {opportunity_value} {currency}")
                print(f"  Timeline: {timeline}")
                print(f"  Products: {product_interest}")
                print(f"  Stage: {opportunity_stage}")
                print(f"  Probability: {probability}")

                # If we couldn't extract ANYTHING meaningful, use default values
                if (company_name == "Unknown Company" and not contact_name and
                    not contact_email and not opportunity_value and not product_interest):
                    print("Extraction failed to find any meaningful data, using dummy data")
                    return CRMOpportunity(
                        company_name="Example Company",
                        contact_name="John Doe",
                        contact_email="john.doe@example.com",
                        opportunity_value=10000,
                        currency="USD",
                        notes="This is dummy data because extraction failed. The text may not contain structured CRM data."
                    )

                return CRMOpportunity(
                    company_name=company_name,
                    contact_name=contact_name,
                    contact_email=contact_email,
                    contact_phone=contact_phone,
                    opportunity_value=opportunity_value,
                    currency=currency,
                    timeline=timeline,
                    product_interest=product_interest if product_interest else None,
                    opportunity_stage=opportunity_stage,
                    probability=probability,
                    notes=notes,
                    # Additional fields
                    location=location if 'location' in locals() else None,
                    project_type=project_type if 'project_type' in locals() else None,
                    industry=industry if 'industry' in locals() else None,
                    product_count=product_count if 'product_count' in locals() else None,
                    design_requirements=design_requirements if 'design_requirements' in locals() else None,
                    integration_requirements=integration_requirements if 'integration_requirements' in locals() and integration_requirements else None,
                    other_requirements=other_requirements if 'other_requirements' in locals() and other_requirements else None
                )
            except Exception as e:
                print(f"Error in dummy extraction: {str(e)}")
                # Fallback to very basic dummy data
                return CRMOpportunity(
                    company_name="Example Company",
                    contact_name="John Doe",
                    contact_email="john.doe@example.com",
                    opportunity_value=10000,
                    currency="USD",
                    notes="This is dummy data because no OpenAI API key was provided."
                )

        try:
            # Run the extraction chain
            result = self.chain.invoke({"document_text": combined_text})

            # Parse the JSON result
            import json

            # Handle different response formats from different LangChain versions
            if isinstance(result, dict) and 'text' in result:
                json_str = result['text']
            elif isinstance(result, str):
                json_str = result
            else:
                json_str = str(result)

            # Clean up the JSON string if needed
            json_str = json_str.strip()
            if json_str.startswith('```json'):
                json_str = json_str[7:]
            if json_str.endswith('```'):
                json_str = json_str[:-3]
            json_str = json_str.strip()

            # Parse the JSON
            crm_data = json.loads(json_str)

            # Create and return a CRMOpportunity object
            return CRMOpportunity(**crm_data)

        except Exception as e:
            raise Exception(f"Error extracting CRM data: {str(e)}")
