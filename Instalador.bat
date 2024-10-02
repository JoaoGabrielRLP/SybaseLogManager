batch
@echo off
setlocal enabledelayedexpansion

echo Verificando se o Python 3 está instalado...
python --version 2>NUL | findstr /R /C:"^Python 3" >NUL
if %ERRORLEVEL% NEQ 0 (
    echo Python 3 não encontrado. Instalando Python 3...
    
    echo Baixando o instalador do Python 3...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe -OutFile python-installer.exe"
    
    if not exist python-installer.exe (
        echo Falha ao baixar o instalador do Python. Saindo...
        pause
        exit /b 1
    )

    echo Instalando Python 3 de forma silenciosa...
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    
    if %ERRORLEVEL% NEQ 0 (
        echo Falha ao instalar o Python. Saindo...
        pause
        exit /b 1
    )

    echo Removendo o instalador...
    del python-installer.exe
)

echo Verificando novamente se o Python 3 foi instalado corretamente...
python --version 2>NUL | findstr /R /C:"^Python 3" >NUL
if %ERRORLEVEL% NEQ 0 (
    echo Falha ao instalar Python 3. Saindo...
    pause
    exit /b 1
)

echo Criando ambiente virtual...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo Falha ao criar o ambiente virtual. Saindo...
    pause
    exit /b 1
)

echo Ativando ambiente virtual...
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo Falha ao ativar o ambiente virtual. Saindo...
    pause
    exit /b 1
)

echo Verificando se o pip está instalado, caso contrário, instalando o pip...
python -m ensurepip --upgrade
if %ERRORLEVEL% NEQ 0 (
    echo Falha ao garantir o pip. Saindo...
    pause
    exit /b 1
)

echo Instalando dependências...
pip install --upgrade pip
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Falha ao instalar dependências. Saindo...
    pause
    exit /b 1
)

echo Instalação completa. Para rodar a aplicação, ative o ambiente virtual com:
echo call venv\Scripts\activate
echo Em seguida, execute:
echo python SybaseLogManager.pyw
pause