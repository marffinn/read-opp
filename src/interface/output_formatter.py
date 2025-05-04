"""
Output Formatter Module

This module formats extracted CRM data into different output formats.
"""

import json
import csv
from io import StringIO
from typing import Dict, Any

def format_as_json(data: Dict[str, Any]) -> str:
    """
    Format CRM data as a JSON string.

    Args:
        data: Dictionary containing CRM data

    Returns:
        Formatted JSON string
    """
    return json.dumps(data.model_dump(), indent=2)

def format_as_csv(data: Dict[str, Any]) -> str:
    """
    Format CRM data as a CSV string.

    Args:
        data: Dictionary containing CRM data

    Returns:
        Formatted CSV string
    """
    # Convert data to dict
    data_dict = data.model_dump()

    # Handle list fields
    for key, value in data_dict.items():
        if isinstance(value, list):
            data_dict[key] = ", ".join(value)

    # Create CSV
    output = StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(data_dict.keys())

    # Write values
    writer.writerow(data_dict.values())

    return output.getvalue()
