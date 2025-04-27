#!/usr/bin/env python3
"""
Initialize Git repository and set up remote connection for the Sultanate Legal AI Assistant project.
"""

import os
import subprocess
import sys

def run_command(command):
    """Run a shell command and print the output."""
    print(f"Running: {command}")
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if process.stdout:
        print(process.stdout)
    
    if process.returncode != 0:
        print(f"Error: {process.stderr}")
        return False
    
    return True

def init_git_repo():
    """Initialize Git repository and set up remote connection."""
    # Check if .git directory already exists
    if os.path.exists(".git"):
        print("Git repository already initialized.")
    else:
        # Initialize git repository
        if not run_command("git init"):
            return False
    
    # Add remote repository
    remote_url = "git@github.com:alanqoudif/Ankaa.git"
    
    # Check if remote already exists
    process = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    if "origin" in process.stdout:
        print(f"Remote 'origin' already exists. Updating to {remote_url}")
        if not run_command(f"git remote set-url origin {remote_url}"):
            return False
    else:
        if not run_command(f"git remote add origin {remote_url}"):
            return False
    
    # Add all files to git
    if not run_command("git add ."):
        return False
    
    # Create initial commit
    if not run_command('git commit -m "Initial commit: Level 1 - Smart Search Bot setup"'):
        return False
    
    print("\nGit repository initialized successfully!")
    print(f"Remote repository set to: {remote_url}")
    print("\nTo push your code to GitHub, run:")
    print("git push -u origin main")
    
    return True

if __name__ == "__main__":
    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    print(f"Initializing Git repository in: {project_dir}")
    if init_git_repo():
        print("\nSetup completed successfully!")
    else:
        print("\nSetup failed. Please check the error messages above.")
        sys.exit(1)
