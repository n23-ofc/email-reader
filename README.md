# IMAP Email Reader

A cross-platform, interactive command-line tool for reading emails from IMAP servers with an fzf-based selection interface.

## Features

- 🔍 Interactive email selection using fzf
- 📧 Support for both plain text and HTML emails
- 🔗 Automatic link extraction and categorization
- 🌍 Cross-platform compatibility (macOS, Linux, Windows)
- 🔐 Secure credential management via environment variables
- 📝 Clean, professional terminal output
- 🛠️ Flexible configuration options

## Prerequisites

### Python Requirements
- Python 3.7 or higher

### External Dependencies
- **fzf**: A command-line fuzzy finder for interactive selection

## Installation

### 1. Clone the Repository

```bash
git clone <https://github.com/n23-ofc/email-reader>
cd email-reader
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or if you prefer using a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Install fzf

#### macOS

Using Homebrew:
```bash
brew install fzf
```

#### Linux

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install fzf
```

**Fedora:**
```bash
sudo dnf install fzf
```

**Arch Linux:**
```bash
sudo pacman -S fzf
```

**Manual Installation (all Linux distros):**
```bash
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

#### Windows

**Using Chocolatey:**
```powershell
choco install fzf
```

**Using Scoop:**
```powershell
scoop install fzf
```

**Manual Installation:**
1. Download the latest release from [fzf releases](https://github.com/junegunn/fzf/releases)
2. Extract the executable to a directory in your PATH
3. Restart your terminal

### 4. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your email credentials:

```env
EMAIL_USER=your.email@example.com
EMAIL_PASS=your_password_here
IMAP_SERVER=imap.example.com
IMAP_PORT=993
```

**Important:** Never commit the `.env` file to version control. It's already included in `.gitignore`.

## Configuration

### Environment Variables

The application uses the following environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `EMAIL_USER` | Yes | - | Your email address |
| `EMAIL_PASS` | Yes | - | Your email password or app-specific password |
| `IMAP_SERVER` | Yes | - | IMAP server hostname (e.g., imap.gmail.com) |
| `IMAP_PORT` | No | 993 | IMAP server port |

### Setting Environment Variables by OS

#### macOS/Linux

**Option 1: Using .env file (recommended)**
```bash
# Create and edit .env file
cp .env.example .env
nano .env  # or use your preferred editor
```

**Option 2: Export in shell**
```bash
export EMAIL_USER="your.email@example.com"
export EMAIL_PASS="your_password"
export IMAP_SERVER="imap.example.com"
```

To make these permanent, add them to your shell profile:
```bash
# For bash: ~/.bashrc or ~/.bash_profile
# For zsh: ~/.zshrc
echo 'export EMAIL_USER="your.email@example.com"' >> ~/.bashrc
```

#### Windows

**Option 1: Using .env file (recommended)**
```powershell
# Copy and edit .env file
copy .env.example .env
notepad .env
```

**Option 2: Set in PowerShell**
```powershell
$env:EMAIL_USER="your.email@example.com"
$env:EMAIL_PASS="your_password"
$env:IMAP_SERVER="imap.example.com"
```

**Option 3: Set System-wide (Permanent)**
```powershell
# Run as Administrator
[System.Environment]::SetEnvironmentVariable('EMAIL_USER', 'your.email@example.com', 'User')
[System.Environment]::SetEnvironmentVariable('EMAIL_PASS', 'your_password', 'User')
[System.Environment]::SetEnvironmentVariable('IMAP_SERVER', 'imap.example.com', 'User')
```

Or use the GUI:
1. Search for "Environment Variables" in Windows
2. Click "Edit environment variables for your account"
3. Add new variables under "User variables"

### Command-Line Arguments

You can also provide configuration via command-line arguments:

```bash
python email_reader.py --user your.email@example.com --server imap.example.com
```

**Note:** Command-line arguments take precedence over environment variables.

## Usage

### Basic Usage

Simply run the script:

```bash
python email_reader.py
```

This will:
1. Connect to your IMAP server
2. Display a list of emails in an interactive fzf menu
3. Show the selected email with extracted links

### Advanced Usage

**With verbose logging:**
```bash
python email_reader.py --verbose
```

**Override configuration:**
```bash
python email_reader.py --user different@email.com --server imap.different.com --port 993
```

**Get help:**
```bash
python email_reader.py --help
```

## Common IMAP Server Settings

### Gmail
```env
EMAIL_USER=your.email@gmail.com
EMAIL_PASS=your_app_password  # Use App Password, not regular password
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
```

**Note:** For Gmail, you need to:
1. Enable 2-factor authentication
2. Generate an [App Password](https://support.google.com/accounts/answer/185833)
3. Use the App Password instead of your regular password

### Outlook/Office 365
```env
EMAIL_USER=your.email@outlook.com
EMAIL_PASS=your_password
IMAP_SERVER=outlook.office365.com
IMAP_PORT=993
```

### Yahoo Mail
```env
EMAIL_USER=your.email@yahoo.com
EMAIL_PASS=your_app_password  # Generate from Yahoo account settings
IMAP_SERVER=imap.mail.yahoo.com
IMAP_PORT=993
```

### iCloud Mail
```env
EMAIL_USER=your.email@icloud.com
EMAIL_PASS=your_app_password  # Generate from iCloud settings
IMAP_SERVER=imap.mail.me.com
IMAP_PORT=993
```

## Troubleshooting

### "fzf is not installed" Error

Make sure fzf is properly installed and in your system PATH:

```bash
# Test if fzf is installed
fzf --version
```

If not found, refer to the [fzf installation instructions](#3-install-fzf) above.

### "Configuration Error" Messages

Ensure all required environment variables are set:

```bash
# Check if variables are set (macOS/Linux)
echo $EMAIL_USER
echo $IMAP_SERVER

# Check if variables are set (Windows PowerShell)
echo $env:EMAIL_USER
echo $env:IMAP_SERVER
```

### "IMAP Error: Authentication failed"

Common causes:
1. **Incorrect credentials**: Double-check your email and password
2. **2FA enabled**: Use an app-specific password instead of your regular password
3. **IMAP not enabled**: Check your email provider's settings to ensure IMAP is enabled
4. **Wrong server**: Verify the IMAP server address for your provider

### SSL/TLS Certificate Errors

If you encounter SSL certificate errors, ensure:
1. Your system's CA certificates are up to date
2. You're using the correct IMAP server address
3. Port 993 is not blocked by your firewall

### No Emails Displayed

Check:
1. The INBOX has emails
2. Your credentials have appropriate permissions
3. Try with `--verbose` flag to see detailed logs

### Windows-Specific Issues

**Terminal encoding issues:**
```powershell
# Set UTF-8 encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

**fzf not working in cmd.exe:**
- Use PowerShell or Windows Terminal instead
- cmd.exe may have limited support for interactive tools

## Security Best Practices

1. **Never commit credentials**: The `.gitignore` file prevents `.env` from being committed
2. **Use app-specific passwords**: Most providers support app-specific passwords that are safer than your main password
3. **Restrict file permissions** on your `.env` file:
   ```bash
   # macOS/Linux
   chmod 600 .env
   ```
4. **Use environment variables** or secure credential stores for production use
5. **Regularly rotate passwords**: Update your credentials periodically

## Development

### Running Tests

```bash
# Run with verbose output for debugging
python email_reader.py --verbose
```

### Code Style

This project follows PEP 8 style guidelines. To check code style:

```bash
pip install flake8
flake8 email_reader.py
```

### Type Checking

```bash
pip install mypy
mypy email_reader.py
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- [fzf](https://github.com/junegunn/fzf) - Command-line fuzzy finder
- [python-dotenv](https://github.com/theskumar/python-dotenv) - .env file support

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the [Troubleshooting](#troubleshooting) section
- Review existing issues for solutions

## Changelog

### Version 1.0.0
- Initial release
- Cross-platform support (macOS, Linux, Windows)
- Interactive email selection with fzf
- HTML and plain text email support
- Link extraction and categorization
- Environment variable configuration
- Comprehensive documentation
