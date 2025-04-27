"""
Utility functions for working with Ollama models in the Legal AI Assistant.
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional

def list_ollama_models() -> List[Dict[str, Any]]:
    """
    Get a list of available Ollama models.
    
    Returns:
        List of dictionaries with model information
    """
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            data = response.json()
            return data.get("models", [])
        else:
            print(f"Error fetching Ollama models: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error connecting to Ollama: {str(e)}")
        return []

def get_ollama_model_info(model_name: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a specific Ollama model.
    
    Args:
        model_name: Name of the Ollama model
        
    Returns:
        Dictionary with model information or None if model not found
    """
    models = list_ollama_models()
    for model in models:
        if model.get("name") == model_name:
            return model
    return None

def generate_ollama_completion(
    model_name: str,
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.1,
    max_tokens: int = 2000,
    stop: Optional[List[str]] = None
) -> str:
    """
    Generate a completion using an Ollama model.
    
    Args:
        model_name: Name of the Ollama model
        prompt: User prompt
        system_prompt: Optional system prompt
        temperature: Temperature parameter
        max_tokens: Maximum number of tokens to generate
        stop: Optional list of stop sequences
        
    Returns:
        Generated text
    """
    try:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        if stop:
            payload["options"]["stop"] = stop
        
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "")
        else:
            error_msg = f"Error generating completion: {response.status_code}"
            print(error_msg)
            return error_msg
    except Exception as e:
        error_msg = f"Error connecting to Ollama: {str(e)}"
        print(error_msg)
        return error_msg

def is_ollama_running() -> bool:
    """
    Check if Ollama is running.
    
    Returns:
        True if Ollama is running, False otherwise
    """
    try:
        response = requests.get("http://localhost:11434/api/tags")
        return response.status_code == 200
    except:
        return False


if __name__ == "__main__":
    # Example usage
    if is_ollama_running():
        print("Ollama is running")
        models = list_ollama_models()
        print(f"Available models: {[model.get('name') for model in models]}")
        
        # Test completion
        if models:
            model_name = models[0].get("name")
            completion = generate_ollama_completion(
                model_name=model_name,
                prompt="What is the capital of Oman?",
                system_prompt="You are a helpful assistant that provides accurate information."
            )
            print(f"Completion from {model_name}: {completion}")
    else:
        print("Ollama is not running. Please start Ollama and try again.")
