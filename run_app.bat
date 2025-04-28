@echo off
REM Script to run the Ankaa Legal AI Assistant application on Windows

echo Activating virtual environment...
IF EXIST .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) ELSE (
    echo Virtual environment not found. Will use system Python.
)

echo Installing/updating dependencies...
pip install -r requirements.txt

echo Starting Ankaa Legal AI Assistant...
streamlit run src/app.py

IF EXIST .venv\Scripts\activate.bat (
    call deactivate
)
