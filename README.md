# Shell-AI: AI-Powered Command Generator

## Overview
Shell-AI is a Python-based AI-powered command generator tool designed for systems and servers where GUI access is unavailable. It helps users generate terminal commands based on their requests using an AI model. This is particularly useful when you forget a specific command but still need to execute tasks efficiently.

## Features
- Detects OS and distribution information.
- Identifies the system's default shell and package manager.
- Uses AI to generate the most appropriate command based on user input.
- Works seamlessly on Linux, macOS, and Windows.
- Simple and interactive CLI interface.

## Installation
### Prerequisites
- Ensure you have Python 3 installed on your system.
- Generate a Groq AI API key from [Groq Console](https://console.groq.com/keys) and set it in the environment variable `GROQ_API_KEY`.

### Install Required Dependencies
```bash
pip install -r requirements.txt
```

## Usage
Run the script using the following command:
```bash
python3 shell-ai.py
```
After execution, type your request (e.g., "create a new user") and get an AI-suggested command for your system.

To exit the tool, type `exit` or `quit`.

## Example Output
```
~> System: Ubuntu 22.04 (Linux)
~> Shell: bash
~> Package Manager: apt
~> Type your request or 'exit'

~> List all files in the current directory
🧠 Processing...

Suggested Command:
ls -l
```

## License
This project is open-source and free to use.

---

