#!/usr/bin/env python3
"""
IMAP Email Reader with Interactive Selection

A cross-platform command-line tool for reading emails from IMAP servers
with an interactive fzf-based selection interface.

Author: n23
License: MIT
"""

import imaplib
import email
from email.header import decode_header
import subprocess
import sys
import os
import re
import logging
import argparse
from pathlib import Path
from html.parser import HTMLParser
from typing import Tuple, List, Optional

# Optional: python-dotenv for .env file support
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False


class HTMLToText(HTMLParser):
    """
    HTML to text converter that extracts readable content and links.
    
    This parser strips HTML tags while preserving text content and
    extracting all hyperlinks found in the HTML.
    """
    
    def __init__(self):
        """Initialize the HTML parser with empty text and link lists."""
        super().__init__()
        self.text = []
        self.links = []
        self.skip = False
        self.current_link = None
    
    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str]]) -> None:
        """
        Handle HTML opening tags.
        
        Args:
            tag: The HTML tag name
            attrs: List of (attribute, value) tuples
        """
        if tag in ['script', 'style']:
            self.skip = True
        elif tag == 'br':
            self.text.append('\n')
        elif tag == 'p':
            self.text.append('\n\n')
        elif tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.current_link = value
                    break
    
    def handle_endtag(self, tag: str) -> None:
        """
        Handle HTML closing tags.
        
        Args:
            tag: The HTML tag name
        """
        if tag in ['script', 'style']:
            self.skip = False
        elif tag in ['p', 'div']:
            self.text.append('\n')
        elif tag == 'a' and self.current_link:
            self.links.append(self.current_link)
            self.current_link = None
    
    def handle_data(self, data: str) -> None:
        """
        Handle text data within HTML tags.
        
        Args:
            data: Text content from HTML
        """
        if not self.skip:
            self.text.append(data)
    
    def get_text(self) -> str:
        """
        Get the extracted plain text.
        
        Returns:
            Plain text content from HTML
        """
        return ''.join(self.text)
    
    def get_links(self) -> List[str]:
        """
        Get all extracted links.
        
        Returns:
            List of URLs found in the HTML
        """
        return self.links


def html_to_text(html: str) -> Tuple[str, List[str]]:
    """
    Convert HTML to plain text and extract links.
    
    Args:
        html: HTML content as string
        
    Returns:
        Tuple of (plain_text, list_of_links)
    """
    parser = HTMLToText()
    parser.feed(html)
    text = parser.get_text()
    # Clean up excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip(), parser.get_links()


def get_clean_text(msg: email.message.Message) -> Tuple[str, List[str]]:
    """
    Extract text content from email message.
    
    Handles both plain text and HTML emails, preferring plain text
    when available. Also extracts all URLs found in the content.
    
    Args:
        msg: Email message object
        
    Returns:
        Tuple of (email_text, list_of_links)
    """
    plain_text = None
    html_text = None
    links = []
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            if "attachment" not in content_disposition:
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        decoded = payload.decode('utf-8', errors='ignore')
                        
                        if content_type == "text/plain":
                            plain_text = decoded
                        elif content_type == "text/html":
                            html_text = decoded
                except Exception as e:
                    logging.debug(f"Error decoding email part: {e}")
    else:
        content_type = msg.get_content_type()
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                decoded = payload.decode('utf-8', errors='ignore')
                
                if content_type == "text/plain":
                    plain_text = decoded
                elif content_type == "text/html":
                    html_text = decoded
        except Exception as e:
            logging.debug(f"Error decoding email: {e}")
    
    # Process the content
    if plain_text and plain_text.strip():
        # Extract URLs from plain text using regex
        links = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', plain_text)
        return plain_text, links
    elif html_text:
        text, links = html_to_text(html_text)
        return text, links
    else:
        return "No readable content found in this email.", []


def clear_terminal() -> None:
    """Clear the terminal screen in a cross-platform way."""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # macOS and Linux
        os.system('clear')


def check_fzf_installed() -> bool:
    """
    Check if fzf is installed and available in PATH.
    
    Returns:
        True if fzf is installed, False otherwise
    """
    try:
        subprocess.run(['fzf', '--version'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL,
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def print_fzf_installation_instructions() -> None:
    """Print platform-specific installation instructions for fzf."""
    print("\n" + "=" * 60)
    print("ERROR: fzf is not installed")
    print("=" * 60)
    print("\nfzf is required for interactive email selection.")
    print("\nInstallation instructions:\n")
    
    if sys.platform == 'darwin':  # macOS
        print("macOS:")
        print("  brew install fzf")
    elif sys.platform == 'win32':  # Windows
        print("Windows:")
        print("  Using Chocolatey: choco install fzf")
        print("  Using Scoop: scoop install fzf")
        print("  Or download from: https://github.com/junegunn/fzf/releases")
    else:  # Linux
        print("Linux:")
        print("  Ubuntu/Debian: sudo apt install fzf")
        print("  Fedora: sudo dnf install fzf")
        print("  Arch: sudo pacman -S fzf")
        print("  Or use: git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf")
        print("           ~/.fzf/install")
    
    print("\nAfter installation, restart your terminal and try again.")
    print("=" * 60)


def decode_email_header(header_value: str) -> str:
    """
    Decode email header with proper encoding handling.
    
    Args:
        header_value: Raw header value
        
    Returns:
        Decoded string
    """
    if not header_value:
        return ""
    
    decoded_parts = decode_header(header_value)
    result = []
    
    for content, encoding in decoded_parts:
        if isinstance(content, bytes):
            try:
                result.append(content.decode(encoding or "utf-8", errors="ignore"))
            except (LookupError, AttributeError):
                result.append(content.decode("utf-8", errors="ignore"))
        else:
            result.append(str(content))
    
    return "".join(result)


def categorize_link(url: str) -> str:
    """
    Categorize a URL based on its content.
    
    Args:
        url: The URL to categorize
        
    Returns:
        Category label for the link
    """
    url_lower = url.lower()
    
    # Check for common patterns
    if any(keyword in url_lower for keyword in ['confirm', 'verify', 'activate', 'validation']):
        return "[VERIFICATION LINK]"
    elif any(keyword in url_lower for keyword in ['unsubscribe', 'opt-out', 'remove']):
        return "[UNSUBSCRIBE LINK]"
    elif any(keyword in url_lower for keyword in ['track', 'pixel', 'beacon']):
        return "[TRACKING LINK]"
    elif any(keyword in url_lower for keyword in ['facebook', 'twitter', 'linkedin', 'instagram']):
        return "[SOCIAL MEDIA]"
    else:
        return "[LINK]"


def load_configuration(args: argparse.Namespace) -> dict:
    """
    Load configuration from environment variables or command-line arguments.
    
    Priority: Command-line args > Environment variables > Defaults
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Dictionary with configuration values
        
    Raises:
        ValueError: If required configuration is missing
    """
    # Load .env file if available
    if DOTENV_AVAILABLE:
        env_path = Path('.env')
        if env_path.exists():
            load_dotenv(env_path)
            logging.info(f"Loaded configuration from {env_path}")
    
    config = {
        'email_user': args.user or os.getenv('EMAIL_USER'),
        'email_pass': args.password or os.getenv('EMAIL_PASS'),
        'imap_server': args.server or os.getenv('IMAP_SERVER'),
        'imap_port': args.port or int(os.getenv('IMAP_PORT', '993')),
    }
    
    # Validate required fields
    if not config['email_user']:
        raise ValueError("Email username not provided. Set EMAIL_USER environment variable or use --user")
    if not config['email_pass']:
        raise ValueError("Email password not provided. Set EMAIL_PASS environment variable or use --password")
    if not config['imap_server']:
        raise ValueError("IMAP server not provided. Set IMAP_SERVER environment variable or use --server")
    
    return config


def connect_to_imap(config: dict) -> imaplib.IMAP4_SSL:
    """
    Connect to IMAP server and login.
    
    Args:
        config: Configuration dictionary with connection details
        
    Returns:
        Connected and authenticated IMAP4_SSL object
        
    Raises:
        imaplib.IMAP4.error: If connection or login fails
    """
    try:
        logging.info(f"Connecting to {config['imap_server']}:{config['imap_port']}")
        mail = imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'])
        mail.login(config['email_user'], config['email_pass'])
        logging.info("Successfully connected and authenticated")
        return mail
    except imaplib.IMAP4.error as e:
        logging.error(f"IMAP connection/login failed: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during connection: {e}")
        raise


def fetch_email_list(mail: imaplib.IMAP4_SSL) -> List[str]:
    """
    Fetch list of email headers for menu display.
    
    Args:
        mail: Connected IMAP4_SSL object
        
    Returns:
        List of formatted email header strings
        
    Raises:
        imaplib.IMAP4.error: If fetching fails
    """
    mail.select("INBOX")
    
    status, messages = mail.search(None, "ALL")
    if status != "OK" or not messages[0]:
        return []
    
    mail_ids = messages[0].split()
    menu_lines = []
    
    for num in mail_ids:
        try:
            res, data = mail.fetch(num, "(BODY[HEADER.FIELDS (FROM SUBJECT DATE)])")
            if res == "OK" and data[0]:
                msg = email.message_from_bytes(data[0][1])
                
                subject = decode_email_header(msg.get("Subject", "No Subject"))
                from_sender = decode_email_header(msg.get("From", "Unknown"))
                
                line = f"{num.decode()}: From: {from_sender} | Subject: {subject}"
                menu_lines.append(line)
        except Exception as e:
            logging.warning(f"Error fetching email {num}: {e}")
            continue
    
    # Reverse so newest is at top
    menu_lines.reverse()
    return menu_lines


def select_email_with_fzf(menu_lines: List[str]) -> Optional[str]:
    """
    Display email list in fzf for interactive selection.
    
    Args:
        menu_lines: List of formatted email headers
        
    Returns:
        Selected email ID or None if cancelled
        
    Raises:
        FileNotFoundError: If fzf is not installed
    """
    fzf_input = "\n".join(menu_lines)
    
    try:
        proc = subprocess.Popen(
            ['fzf', '--prompt=Select an email to read: ', '--height=40%'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        selected, stderr = proc.communicate(input=fzf_input)
        
        if proc.returncode != 0:
            if proc.returncode == 130:  # User cancelled (Ctrl+C)
                return None
            logging.error(f"fzf error: {stderr}")
            return None
        
        return selected.strip()
    except FileNotFoundError:
        raise


def display_email(mail: imaplib.IMAP4_SSL, email_id: str) -> None:
    """
    Fetch and display the full email content.
    
    Args:
        mail: Connected IMAP4_SSL object
        email_id: Email ID to fetch
    """
    res, data = mail.fetch(email_id, "(RFC822)")
    if res != "OK" or not data[0]:
        print(f"Error: Could not fetch email {email_id}")
        return
    
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)
    
    # Display email
    clear_terminal()
    print("=" * 60)
    print(f" EMAIL ID: {email_id}")
    print("=" * 60)
    print(f"From: {decode_email_header(msg.get('From', 'Unknown'))}")
    print(f"Subject: {decode_email_header(msg.get('Subject', 'No Subject'))}")
    print(f"Date: {msg.get('Date', 'Unknown')}")
    print("=" * 60)
    print()
    
    text, links = get_clean_text(msg)
    print(text.strip())
    
    # Display extracted links
    if links:
        print("\n" + "=" * 60)
        print(" LINKS FOUND IN EMAIL:")
        print("=" * 60)
        
        for i, link in enumerate(links, 1):
            category = categorize_link(link)
            print(f"\n{i}. {category}")
            print(f"   {link}")
    
    print("\n" + "=" * 60)


def setup_logging(verbose: bool = False) -> None:
    """
    Configure logging based on verbosity level.
    
    Args:
        verbose: If True, set log level to DEBUG
    """
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description='Interactive IMAP email reader with fzf selection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --user myemail@example.com --server imap.example.com
  %(prog)s --verbose

Environment Variables:
  EMAIL_USER      Email address for IMAP login
  EMAIL_PASS      Password for IMAP login
  IMAP_SERVER     IMAP server hostname
  IMAP_PORT       IMAP server port (default: 993)

Configuration can also be loaded from a .env file in the current directory.
        """
    )
    
    parser.add_argument(
        '-u', '--user',
        help='Email address (overrides EMAIL_USER environment variable)'
    )
    parser.add_argument(
        '-p', '--password',
        help='Email password (overrides EMAIL_PASS environment variable)'
    )
    parser.add_argument(
        '-s', '--server',
        help='IMAP server hostname (overrides IMAP_SERVER environment variable)'
    )
    parser.add_argument(
        '--port',
        type=int,
        help='IMAP server port (default: 993)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()


def main() -> int:
    """
    Main entry point for the email reader.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    args = parse_arguments()
    setup_logging(args.verbose)
    
    # Check for fzf
    if not check_fzf_installed():
        print_fzf_installation_instructions()
        return 1
    
    try:
        # Load configuration
        config = load_configuration(args)
        
        # Connect to IMAP server
        mail = connect_to_imap(config)
        
        try:
            # Fetch email list
            menu_lines = fetch_email_list(mail)
            
            if not menu_lines:
                print("No emails found in your inbox.")
                return 0
            
            # Interactive selection
            selected = select_email_with_fzf(menu_lines)
            
            if not selected:
                logging.info("No email selected or selection cancelled")
                return 0
            
            # Extract email ID from selection
            selected_id = selected.split(":")[0]
            
            # Display the email
            display_email(mail, selected_id)
            
        finally:
            # Always close the connection
            try:
                mail.close()
                mail.logout()
            except Exception as e:
                logging.debug(f"Error during IMAP cleanup: {e}")
        
        return 0
        
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        print("\nPlease ensure you have set the required environment variables")
        print("or provided them as command-line arguments.")
        print("\nRun with --help for more information.")
        return 1
    
    except imaplib.IMAP4.error as e:
        print(f"\nIMAP Error: {e}")
        print("\nPlease check your credentials and server settings.")
        return 1
    
    except FileNotFoundError:
        print_fzf_installation_instructions()
        return 1
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 0
    
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=args.verbose)
        print(f"\nAn unexpected error occurred: {e}")
        if not args.verbose:
            print("Run with --verbose flag for more details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
