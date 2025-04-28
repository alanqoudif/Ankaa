# Deployment Guide for Sultanate Legal AI Assistant

This guide explains how to deploy the Sultanate Legal AI Assistant to Streamlit Cloud.

## Prerequisites

1. A GitHub account
2. Your repository pushed to GitHub (already done)
3. An OpenRouter API key

## Deployment Steps

### 1. Sign up for Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign up using your GitHub account
2. Authorize Streamlit to access your GitHub repositories

### 2. Deploy Your App

1. Click on "New app" in the Streamlit Cloud dashboard
2. Select your GitHub repository (`alanqoudif/Ankaa`)
3. Configure the deployment:
   - **Main file path**: `src/app.py`
   - **Branch**: `master` (or `main` if you renamed it)
   - **Python version**: 3.10
   - **Advanced settings**: Add the following secrets
     - `OPENROUTER_API_KEY`: Your OpenRouter API key

### 3. Environment Variables

In the "Advanced settings" section, add the following secrets:

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
DEFAULT_MODEL=openai/gpt-4-turbo
```

### 4. Deploy

Click "Deploy" and wait for the deployment process to complete. This may take a few minutes as Streamlit installs all the dependencies.

### 5. Access Your App

Once deployed, you'll receive a URL where your app is accessible (typically `https://username-repo-name.streamlit.app`).

## Important Notes

1. **Voice Recognition**: The voice recognition features may have limited functionality in the cloud deployment due to microphone access restrictions in web browsers.

2. **Storage**: Streamlit Cloud has ephemeral storage, meaning files uploaded or created during a session might not persist. Consider using cloud storage solutions for persistent data.

3. **Memory Usage**: If your app exceeds the memory limits of Streamlit Cloud's free tier, you might need to optimize your code or consider a paid hosting solution.

4. **Secrets Management**: Never hardcode API keys in your code. Always use Streamlit's secrets management as described above.

## Troubleshooting

If you encounter issues during deployment:

1. Check the logs in the Streamlit Cloud dashboard
2. Ensure all dependencies are correctly listed in `requirements.txt`
3. Verify that your `.env` file is not being pushed to GitHub (it should be in `.gitignore`)
4. Make sure your app works locally before deploying
