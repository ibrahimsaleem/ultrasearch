@echo off
echo 🚀 Starting UltraSearch - Lightning Fast RAG Search...
echo 📱 App will be available at: http://localhost:8501
echo ⏹️  Press Ctrl+C to stop
echo.
echo ✨ Features:
echo   ⚡ Lightning fast search with RAG
echo   🧠 AI-powered embeddings
echo   📁 Multi-folder indexing
echo   🔍 Smart content search
echo   📊 Real-time performance metrics
echo   🤖 AI analysis of results
echo.

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Install dependencies if needed
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found!
    pause
    exit /b 1
)

echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Run the app
python start.py

pause