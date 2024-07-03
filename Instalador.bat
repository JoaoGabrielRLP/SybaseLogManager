@echo off

:: Verifica se o Python 3 está instalado
python --version 2>NUL | findstr /R /C:"^Python 3" >NUL
if %ERRORLEVEL% NEQ 0 (
    echo Python 3 não encontrado. Instalando Python 3...
    
    :: Baixa o instalador do Python 3
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe -OutFile python-installer.exe"
    
    :: Instala o Python 3 de forma silenciosa
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    
    :: Remove o instalador
    del python-installer.exe
)

:: Verifica novamente se o Python 3 foi instalado corretamente
python --version 2>NUL | findstr /R /C:"^Python 3" >NUL
if %ERRORLEVEL% NEQ 0 (
    echo Falha ao instalar Python 3. Saindo...
    exit /b 1
)

echo Criando ambiente virtual...
python -m venv venv

echo Ativando ambiente virtual...
call venv\Scripts\activate

echo Instalando dependências...
pip install --upgrade pip
pip install -r requirements.txt

echo Instalação completa. Para rodar a aplicação, ative o ambiente virtual com:
echo call venv\Scripts\activate
echo Em seguida, execute:
echo python aplicarlog.pyw
sh
#!/bin/bash

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r get-pip.py

echo "Installation complete. To run the application, activate the virtual environment with:"
echo "source venv/bin/activate"
echo "Then run:"
echo "python aplicarlog.pyw"
