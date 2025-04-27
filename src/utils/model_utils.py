"""
Utility functions for handling LLM models in the Legal AI Assistant.
"""

import os
import sys
import requests
from tqdm import tqdm
from typing import Optional

def download_model(
    model_url: str,
    output_path: str,
    chunk_size: int = 8192,
    force_download: bool = False
) -> bool:
    """
    Download a model file from a URL with progress bar.
    
    Args:
        model_url: URL to download the model from
        output_path: Path to save the model file
        chunk_size: Size of chunks to download
        force_download: Whether to force download even if the file exists
        
    Returns:
        True if download was successful, False otherwise
    """
    # Check if model already exists
    if os.path.exists(output_path) and not force_download:
        print(f"Model already exists at {output_path}. Skipping download.")
        return True
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        # Send a HEAD request to get the file size
        response = requests.head(model_url)
        file_size = int(response.headers.get('content-length', 0))
        
        # Download the file
        response = requests.get(model_url, stream=True)
        response.raise_for_status()
        
        # Show progress bar
        progress_bar = tqdm(
            total=file_size,
            unit='B',
            unit_scale=True,
            desc=f"Downloading {os.path.basename(output_path)}"
        )
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    progress_bar.update(len(chunk))
        
        progress_bar.close()
        
        if os.path.getsize(output_path) != file_size and file_size > 0:
            print(f"Warning: Downloaded file size ({os.path.getsize(output_path)}) doesn't match expected size ({file_size}).")
        
        print(f"Model downloaded successfully to {output_path}")
        return True
    
    except Exception as e:
        print(f"Error downloading model: {str(e)}")
        # Remove partially downloaded file
        if os.path.exists(output_path):
            os.remove(output_path)
        return False

def get_recommended_models() -> list:
    """
    Get a list of recommended models for the Legal AI Assistant.
    
    Returns:
        List of dictionaries with model information
    """
    return [
        {
            "name": "Llama 2 7B Chat (GGML Q4_0)",
            "description": "Llama 2 7B Chat model quantized to 4-bit for efficient CPU inference",
            "size_gb": 3.83,
            "url": "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q4_0.bin",
            "path": "models/llama-2-7b-chat.ggmlv3.q4_0.bin"
        },
        {
            "name": "Mistral 7B Instruct (GGML Q4_0)",
            "description": "Mistral 7B Instruct model quantized to 4-bit for efficient CPU inference",
            "size_gb": 3.83,
            "url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGML/resolve/main/mistral-7b-instruct-v0.1.ggmlv3.q4_0.bin",
            "path": "models/mistral-7b-instruct-v0.1.ggmlv3.q4_0.bin"
        }
    ]

def check_model_availability(model_path: str) -> bool:
    """
    Check if a model file is available at the specified path.
    
    Args:
        model_path: Path to the model file
        
    Returns:
        True if the model is available, False otherwise
    """
    return os.path.exists(model_path) and os.path.getsize(model_path) > 1000000  # At least 1MB


if __name__ == "__main__":
    # Example usage
    models = get_recommended_models()
    for model in models:
        print(f"Model: {model['name']}")
        print(f"Description: {model['description']}")
        print(f"Size: {model['size_gb']} GB")
        print(f"Available: {check_model_availability(model['path'])}")
        print("-" * 50)
