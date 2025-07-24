@echo off
SETLOCAL

REM Navigate to the main project directory
cd /d "%~dp0resume_builder_django"

REM Create virtual environment (if it doesn't exist)
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install project dependencies
if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found!
)

REM Run Django management commands
echo Running makemigrations...
python manage.py makemigrations

echo Running migrate...
python manage.py migrate

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Create superuser (will prompt interactively)
echo Creating superuser (follow prompts)...
python manage.py createsuperuser

REM Check for project issues
echo Running Django checks...
python manage.py check

REM Start development server
echo Starting development server on http://127.0.0.1:8000 ...
python manage.py runserver

ENDLOCAL
pause
