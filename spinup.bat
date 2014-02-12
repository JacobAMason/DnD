@ECHO OFF
start python -i server.py
ping localhost -n 3 >nul
python -i client.py
