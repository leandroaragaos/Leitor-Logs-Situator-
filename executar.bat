@echo off
REM Caminho completo para o Python, caso não esteja no PATH
set PYTHON_PATH=C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe

REM Caminho para o script da aplicação Streamlit
set SCRIPT_PATH="C:\log situator\monitor_log.py"

echo Verificando caminhos...
echo Caminho do Python: %PYTHON_PATH%
echo Caminho do Script: %SCRIPT_PATH%

REM Pausa para ver erros antes de executar o Streamlit
pause

REM Executa o Streamlit usando o Python
"%PYTHON_PATH%" -m streamlit run %SCRIPT_PATH% --server.address=0.0.0.0 --server.port=8501

pause
