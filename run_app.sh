#!/bin/bash
# Script to run the Ankaa Legal AI Assistant application

# Activate virtual environment (if it exists)
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Install or update dependencies
echo "Installing/updating dependencies..."
pip install -r requirements.txt

# Run the Streamlit application
echo "Starting Ankaa Legal AI Assistant..."
streamlit run src/app.py

# Deactivate virtual environment on exit
if [ -d ".venv" ]; then
    deactivate
fi
