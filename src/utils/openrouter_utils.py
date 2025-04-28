"""
OpenRouter API utilities for the Legal AI Assistant.
Provides functions to interact with the OpenRouter API.
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"

def get_openrouter_models() -> List[Dict[str, Any]]:
    """
    Get a list of available models from OpenRouter.
    
    Returns:
        List of model information dictionaries with at least one default model
    """
    # Default models to always include
    default_models = [
        {
            "id": "openai/gpt-3.5-turbo",
            "context_length": 16385,
            "display_name": "OpenAI GPT-3.5 Turbo (16385 tokens)"
        },
        {
            "id": "anthropic/claude-3-haiku",
            "context_length": 200000,
            "display_name": "Anthropic Claude 3 Haiku (200000 tokens)"
        },
        {
            "id": "meta-llama/llama-3-8b-instruct",
            "context_length": 8192,
            "display_name": "Meta Llama 3 8B Instruct (8192 tokens)"
        }
    ]
    
    try:
        # Get API key from environment
        api_key = os.environ.get("OPENROUTER_API_KEY", "")
        
        if not api_key:
            print("Warning: OPENROUTER_API_KEY not found in environment variables")
            return default_models
            
        # Make request to OpenRouter API
        response = requests.get(
            f"{OPENROUTER_API_URL}/models",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://legal-ai-assistant.com",
                "X-Title": "Sultanate Legal AI Assistant"
            }
        )
        
        if response.status_code == 200:
            models_data = response.json()
            
            # Get all available models
            models = models_data.get("data", [])
            
            # Add a display name for each model
            for model in models:
                model['display_name'] = f"{model['id']} ({model.get('context_length', 'unknown')} tokens)"
            
            # Sort models by pricing (free first)
            models.sort(key=lambda x: x.get("pricing", {}).get("prompt", float("inf")))
            
            if models:
                return models
            else:
                print("No models returned from OpenRouter API, using defaults")
                return default_models
        else:
            print(f"Error fetching OpenRouter models: {response.status_code} - {response.text}")
            return default_models
    except Exception as e:
        print(f"Exception while fetching OpenRouter models: {str(e)}")
        return default_models

def generate_openrouter_completion(
    model_id: str,
    prompt: str,
    system_prompt: str = "",
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str:
    """
    Generate a completion using the OpenRouter API.
    
    Args:
        model_id: ID of the model to use
        prompt: User prompt
        system_prompt: System prompt
        temperature: Temperature parameter
        max_tokens: Maximum number of tokens to generate
        
    Returns:
        Generated text
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("OPENROUTER_API_KEY", "")
        
        if not api_key:
            return "Error: OpenRouter API key not found. Please set the OPENROUTER_API_KEY environment variable."
        
        # Print debugging information
        print(f"\nSending to OpenRouter model: {model_id}")
        print(f"System prompt: {system_prompt[:100]}..." if len(system_prompt) > 100 else f"System prompt: {system_prompt}")
        print(f"User prompt: {prompt[:100]}..." if len(prompt) > 100 else f"User prompt: {prompt}")
            
        # Prepare request payload
        payload = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # Make request to OpenRouter API
        response = requests.post(
            f"{OPENROUTER_API_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://legal-ai-assistant.com",  # Replace with your actual domain
                "X-Title": "Sultanate Legal AI Assistant",
                "Content-Type": "application/json"
            },
            json=payload
        )
        
        if response.status_code == 200:
            response_data = response.json()
            # Extract the generated text from the response
            if "choices" in response_data and len(response_data["choices"]) > 0:
                result = response_data["choices"][0]["message"]["content"]
                print(f"OpenRouter response: {result[:100]}..." if len(result) > 100 else f"OpenRouter response: {result}")
                return result
            else:
                print("No choices in OpenRouter response")
                return "No response generated."
        else:
            error_message = f"Error from OpenRouter API: {response.status_code} - {response.text}"
            print(error_message)
            return f"Error: {error_message}"
    except Exception as e:
        error_message = f"Exception during OpenRouter API call: {str(e)}"
        print(error_message)
        return f"Error: {error_message}"

def is_openrouter_available() -> bool:
    """
    Check if OpenRouter API is available.
    
    Returns:
        True if OpenRouter API is available, False otherwise
    """
    try:
        response = requests.get(f"{OPENROUTER_API_URL}/models")
        return response.status_code == 200
    except:
        return False
