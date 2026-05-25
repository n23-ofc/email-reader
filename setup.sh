#!/bin/bash

# IMAP Email Reader - Quick Setup Script
# This script helps you set up the email reader quickly on macOS/Linux

set -e  # Exit on error

echo "=========================================="
echo "  IMAP Email Reader - Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Please install Python 3.7 or higher and try again."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Found Python $PYTHON_VERSION"
echo ""

# Check for pip
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed."
    echo "Please install pip and try again."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "Virtual environment created."
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencies installed."
echo ""

# Check for fzf
echo "Checking for fzf..."
if ! command -v fzf &> /dev/null; then
    echo "WARNING: fzf is not installed."
    echo ""
    echo "fzf is required for interactive email selection."
    echo "Installation instructions:"
    echo ""
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "  macOS (using Homebrew):"
        echo "    brew install fzf"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        echo "  Ubuntu/Debian:"
        echo "    sudo apt update && sudo apt install fzf"
        echo ""
        echo "  Fedora:"
        echo "    sudo dnf install fzf"
        echo ""
        echo "  Manual installation:"
        echo "    git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf"
        echo "    ~/.fzf/install"
    fi
    echo ""
    read -p "Would you like to continue without fzf? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "fzf is installed: $(fzf --version)"
fi
echo ""

# Set up .env file
if [ -f ".env" ]; then
    echo ".env file already exists. Skipping setup..."
else
    echo "Setting up .env file..."
    cp .env.example .env
    echo ".env file created from template."
    echo ""
    echo "IMPORTANT: Edit the .env file with your credentials:"
    echo "  nano .env"
    echo ""
    echo "Required variables:"
    echo "  - EMAIL_USER: Your email address"
    echo "  - EMAIL_PASS: Your password (use app password for Gmail/Yahoo)"
    echo "  - IMAP_SERVER: Your IMAP server (e.g., imap.gmail.com)"
    
    # Secure the .env file
    chmod 600 .env
    echo ""
    echo "Set .env file permissions to 600 (read/write for owner only)"
fi
echo ""

# Make script executable
chmod +x email_reader.py

echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env with your email credentials:"
echo "     nano .env"
echo ""
echo "  2. Run the email reader:"
echo "     source venv/bin/activate"
echo "     python email_reader.py"
echo ""
echo "  Or simply:"
echo "     ./email_reader.py"
echo ""
echo "For help, run:"
echo "  python email_reader.py --help"
echo ""
echo "Happy emailing!"
