#!/usr/bin/env python3

import os
import platform
import readline
import signal
import sys
from colorama import Fore, Style, init
from groq import Groq

# Initialize colorama
init()

# Ensure Groq API Key is set
DEFAULT_API_KEY = "GROQ_API_KEY"

def get_os_info():
    """Detect OS and distribution information with enhanced detection"""
    system = platform.system()
    os_info = {
        'os': system,
        'distro': 'Unknown',
        'shell': os.environ.get('SHELL', '/bin/sh').split('/')[-1],
        'package_manager': 'unknown'
    }

    if system == "Linux":
        try:
            # Try to read distribution info from various files
            for release_file in ['/etc/os-release', '/etc/lsb-release', '/etc/redhat-release']:
                try:
                    with open(release_file, 'r') as f:
                        for line in f:
                            if line.startswith('PRETTY_NAME='):
                                os_info['distro'] = line.split('=', 1)[1].strip().strip('"')
                                break
                            elif line.startswith('NAME='):
                                os_info['distro'] = line.split('=', 1)[1].strip().strip('"')
                            elif line.startswith('DISTRIB_DESCRIPTION='):
                                os_info['distro'] = line.split('=', 1)[1].strip().strip('"')
                except FileNotFoundError:
                    continue

            # Detect package manager
            for cmd, pkg_mgr in [('apt-get', 'apt'), ('dnf', 'dnf'), ('yum', 'yum'), 
                                ('pacman', 'pacman'), ('zypper', 'zypper'), ('emerge', 'portage')]:
                if os.system(f"command -v {cmd} >/dev/null 2>&1") == 0:
                    os_info['package_manager'] = pkg_mgr
                    break

        except Exception:
            pass

    elif system == "Darwin":
        os_info.update({
            'distro': "macOS",
            'package_manager': 'brew'
        })
    elif system == "Windows":
        os_info.update({
            'distro': "Windows",
            'shell': os.environ.get('COMSPEC', 'cmd.exe').split('\\')[-1]
        })
    
    return os_info

def get_command(user_input, os_info):
    """Get command from Groq API with OS context"""
    prompt = (
        f"System Information:\n"
        f"- OS: {os_info['os']}\n"
        f"- Distribution: {os_info['distro']}\n"
        f"- Shell: {os_info['shell']}\n"
        f"- Package Manager: {os_info['package_manager']}\n\n"
        f"User Request: {user_input}\n\n"
        "Provide exactly ONE terminal command to fulfill this request. "
        "Only output the command with no additional explanation or formatting. "
        "Ensure the command is appropriate for the detected system."
    )

    try:
        # Try environment variable first, fall back to default
        api_key = os.environ.get("GROQ_API_KEY", DEFAULT_API_KEY)
        client = Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
            temperature=0.3,  # More deterministic output
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"{Fore.RED}{Style.BRIGHT}Error: {str(e)}{Style.RESET_ALL}"

def signal_handler(sig, frame):
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Exiting...{Style.RESET_ALL}")
    sys.exit(0)

def print_banner():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}")
    print(r"""
    ███████╗██╗  ██╗███████╗██╗     ██╗       █████╗ ██╗
    ██╔════╝██║  ██║██╔════╝██║     ██║      ██╔══██╗██║
    ███████╗███████║█████╗  ██║     ██║█████╗███████║██║
    ╚════██║██╔══██║██╔══╝  ██║     ██║╚════╝██╔══██║██║
    ███████║██║  ██║███████╗███████╗███████╗ ██║  ██║██║
    ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═╝  ╚═╝╚═╝
    """)
    print(f"{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}AI-Powered Command Generator{Style.RESET_ALL}\n")

def main():
    signal.signal(signal.SIGINT, signal_handler)
    os_info = get_os_info()

    print_banner()
    print(f"{Fore.CYAN}{Style.BRIGHT}~> System: {os_info['distro']} ({os_info['os']})")
    print(f"~> Shell: {os_info['shell']}")
    print(f"~> Package Manager: {os_info['package_manager']}")
    print(f"~> Type your request or 'exit'{Style.RESET_ALL}")

    while True:
        try:
            user_input = input(f"{Fore.GREEN}{Style.BRIGHT}~> {Style.RESET_ALL}").strip()
            if user_input.lower() in ["exit", "quit"]:
                print(f"{Fore.YELLOW}{Style.BRIGHT}Exiting... Bye! 👋{Style.RESET_ALL}")
                break
            if not user_input:
                continue

            print(f"{Fore.BLUE}{Style.BRIGHT}🧠 Processing...{Style.RESET_ALL}")
            command = get_command(user_input, os_info)
            
            if command.startswith("Error:"):
                print(command)
            else:
                print(f"\n{Fore.CYAN}{Style.BRIGHT}Suggested Command:{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{command}{Style.RESET_ALL}")
                print()  # Extra newline for better readability

        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}Error: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    # Check if running on Windows for color support
    if platform.system() == "Windows":
        os.system("color")  # Enable ANSI colors on Windows
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Exiting...{Style.RESET_ALL}")
        sys.exit(0)

