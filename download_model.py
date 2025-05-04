#!/usr/bin/env python3
"""
Download the Mistral 7B model for local use.

This script downloads the GGUF version of the Mistral 7B model,
which is optimized for CPU and GPU inference.
"""

import os
import sys
from huggingface_hub import hf_hub_download
from pathlib import Path

def download_model():
    """Download the Mistral 7B model."""
    print("Downloading Mistral 7B model (GGUF format)...")
    
    # Create models directory if it doesn't exist
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Model information
    repo_id = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
    filename = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"  # Q4 quantization for balance of quality and size
    
    # Check if model already exists
    local_path = models_dir / filename
    if local_path.exists():
        print(f"Model already exists at {local_path}")
        return str(local_path)
    
    try:
        # Download the model
        model_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=models_dir,
            local_dir_use_symlinks=False
        )
        
        print(f"Model downloaded successfully to: {model_path}")
        return model_path
        
    except Exception as e:
        print(f"Error downloading model: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    download_model()
