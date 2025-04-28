#!/bin/bash

# Deployment helper script for Sultanate Legal AI Assistant

echo "Preparing for deployment..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed. Please install git and try again."
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree &> /dev/null; then
    echo "Error: Not in a git repository. Please run this script from the root of your project."
    exit 1
fi

# Make sure all changes are committed
if ! git diff-index --quiet HEAD --; then
    echo "You have uncommitted changes. Would you like to commit them? (y/n)"
    read -r answer
    if [ "$answer" = "y" ]; then
        echo "Enter commit message:"
        read -r commit_message
        git add .
        git commit -m "$commit_message"
    else
        echo "Please commit your changes before deploying."
        exit 1
    fi
fi

# Push to GitHub
echo "Pushing to GitHub..."
git push origin master

echo "Deployment preparation complete!"
echo "Now follow these steps to deploy to Streamlit Cloud:"
echo "1. Go to https://streamlit.io/cloud"
echo "2. Sign in with your GitHub account"
echo "3. Click 'New app'"
echo "4. Select your repository (alanqoudif/Ankaa)"
echo "5. Set the main file path to 'src/app.py'"
echo "6. Add your secrets (OPENROUTER_API_KEY) in the Advanced Settings"
echo "7. Click 'Deploy'"
echo ""
echo "For more detailed instructions, see DEPLOYMENT.md"
