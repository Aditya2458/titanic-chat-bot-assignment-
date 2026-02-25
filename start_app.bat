@echo off
echo Starting Titanic Chatbot...
echo.

echo Starting FastAPI Backend (accessible on network)...
start "Titanic Backend" cmd /k "cd /d c:\Users\itsme\Desktop\titanic-chatbot && python main.py"

timeout /t 3 /nobreak >nul

echo Starting Streamlit Frontend (accessible on network)...
start "Titanic Streamlit" cmd /k "streamlit run c:\Users\itsme\Desktop\titanic-chatbot\app.py --server.headless true --server.address 0.0.0.0"

echo.
echo Titanic Chatbot is starting!
echo.
echo Access URLs (from this computer):
echo   - Backend API: http://localhost:8000
echo   - Frontend:   http://localhost:8501
echo.
echo Access URLs (from other devices on your network):
echo   - Frontend:   http://YOUR_IP_ADDRESS:8501
echo.
echo To find your IP address, run: ipconfig
echo.
echo Close these command windows to stop the servers.
pause
