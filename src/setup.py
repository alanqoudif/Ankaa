"""
Setup script for the Sultanate Legal AI Assistant.
Helps with downloading models and setting up the environment.
"""

import os
import sys
import argparse
from utils.model_utils import download_model, get_recommended_models, check_model_availability

def setup_environment():
    """Create necessary directories for the project."""
    directories = [
        "src/data",
        "models",
        "chroma_db"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def list_models():
    """List recommended models for the Legal AI Assistant."""
    models = get_recommended_models()
    
    print("\nRecommended Models:")
    print("-" * 80)
    for i, model in enumerate(models, 1):
        status = "Available" if check_model_availability(model["path"]) else "Not Downloaded"
        print(f"{i}. {model['name']} ({model['size_gb']} GB) - {status}")
        print(f"   Description: {model['description']}")
        print(f"   Path: {model['path']}")
        print("-" * 80)

def download_selected_model(model_index=None):
    """Download a selected model."""
    models = get_recommended_models()
    
    if model_index is None:
        list_models()
        try:
            selection = int(input("\nEnter the number of the model to download (0 to cancel): "))
            if selection == 0:
                return
            if selection < 1 or selection > len(models):
                print("Invalid selection.")
                return
            model = models[selection - 1]
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
    else:
        if model_index < 1 or model_index > len(models):
            print("Invalid model index.")
            return
        model = models[model_index - 1]
    
    print(f"\nDownloading {model['name']}...")
    print(f"This will download approximately {model['size_gb']} GB of data.")
    confirmation = input("Continue? (y/n): ").lower()
    
    if confirmation == 'y':
        success = download_model(model['url'], model['path'])
        if success:
            print(f"\nModel downloaded successfully to {model['path']}")
        else:
            print("\nFailed to download model. Please check your internet connection and try again.")
    else:
        print("\nDownload cancelled.")

def check_data_directory():
    """Check if there are PDF files in the data directory."""
    data_dir = "src/data"
    if not os.path.exists(data_dir):
        print(f"Data directory {data_dir} does not exist.")
        return False
    
    pdf_files = [f for f in os.listdir(data_dir) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"No PDF files found in {data_dir}. Please add some legal documents.")
        return False
    
    print(f"Found {len(pdf_files)} PDF files in {data_dir}:")
    for pdf_file in pdf_files:
        print(f"- {pdf_file}")
    
    return True

def main():
    """Main function for the setup script."""
    parser = argparse.ArgumentParser(description="Setup the Sultanate Legal AI Assistant")
    parser.add_argument("--download-model", type=int, help="Download a specific model by index")
    parser.add_argument("--list-models", action="store_true", help="List recommended models")
    parser.add_argument("--check-data", action="store_true", help="Check data directory for PDF files")
    parser.add_argument("--setup", action="store_true", help="Setup the environment")
    
    args = parser.parse_args()
    
    if args.setup or len(sys.argv) == 1:
        setup_environment()
    
    if args.list_models or len(sys.argv) == 1:
        list_models()
    
    if args.download_model:
        download_selected_model(args.download_model)
    
    if args.check_data or len(sys.argv) == 1:
        check_data_directory()

if __name__ == "__main__":
    main()
