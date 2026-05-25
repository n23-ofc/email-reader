# IMAP Email Reader - Quick Setup Script for Windows
# Run this script in PowerShell to set up the email reader

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  IMAP Email Reader - Setup Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.7 or higher from https://www.python.org/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Check for pip
Write-Host "Checking for pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "Found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: pip is not installed." -ForegroundColor Red
    Write-Host "Please reinstall Python with pip included." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Skipping..." -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "Virtual environment created." -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host "Dependencies installed." -ForegroundColor Green
Write-Host ""

# Check for fzf
Write-Host "Checking for fzf..." -ForegroundColor Yellow
$fzfInstalled = $false
try {
    $fzfVersion = fzf --version 2>&1
    Write-Host "fzf is installed: $fzfVersion" -ForegroundColor Green
    $fzfInstalled = $true
} catch {
    Write-Host "WARNING: fzf is not installed." -ForegroundColor Red
    Write-Host ""
    Write-Host "fzf is required for interactive email selection." -ForegroundColor Yellow
    Write-Host "Installation options:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  1. Using Chocolatey:" -ForegroundColor Cyan
    Write-Host "     choco install fzf" -ForegroundColor White
    Write-Host ""
    Write-Host "  2. Using Scoop:" -ForegroundColor Cyan
    Write-Host "     scoop install fzf" -ForegroundColor White
    Write-Host ""
    Write-Host "  3. Manual download:" -ForegroundColor Cyan
    Write-Host "     https://github.com/junegunn/fzf/releases" -ForegroundColor White
    Write-Host ""
    
    $continue = Read-Host "Continue without fzf? (y/n)"
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        exit 1
    }
}
Write-Host ""

# Set up .env file
if (Test-Path ".env") {
    Write-Host ".env file already exists. Skipping setup..." -ForegroundColor Green
} else {
    Write-Host "Setting up .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host ".env file created from template." -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT: Edit the .env file with your credentials:" -ForegroundColor Yellow
    Write-Host "  notepad .env" -ForegroundColor White
    Write-Host ""
    Write-Host "Required variables:" -ForegroundColor Yellow
    Write-Host "  - EMAIL_USER: Your email address" -ForegroundColor White
    Write-Host "  - EMAIL_PASS: Your password (use app password for Gmail/Yahoo)" -ForegroundColor White
    Write-Host "  - IMAP_SERVER: Your IMAP server (e.g., imap.gmail.com)" -ForegroundColor White
}
Write-Host ""

# Summary
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "  1. Edit .env with your email credentials:" -ForegroundColor Yellow
Write-Host "     notepad .env" -ForegroundColor White
Write-Host ""
Write-Host "  2. Activate the virtual environment:" -ForegroundColor Yellow
Write-Host "     venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "  3. Run the email reader:" -ForegroundColor Yellow
Write-Host "     python email_reader.py" -ForegroundColor White
Write-Host ""
Write-Host "For help, run:" -ForegroundColor Yellow
Write-Host "  python email_reader.py --help" -ForegroundColor White
Write-Host ""
Write-Host "Happy emailing!" -ForegroundColor Green
