!/bin/bash

# Ensure Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Installing Python..."
    if [ -f /etc/debian_version ]; then
        sudo apt update && sudo apt install python3 python3-pip -y
    elif [ -f /etc/redhat-release ]; then
        sudo dnf install python3 python3-pip -y
    else
        echo "Unsupported Linux distribution. Install Python manually."
        exit 1
    fi
fi

# Verify pip installation
if ! command -v pip3 &> /dev/null
then
    echo "pip is not installed. Installing pip..."
    sudo apt install python3-pip -y || sudo dnf install python3-pip -y
fi

# Install pip dependencies
pip3 install subprocess-tee argparse textwrap logging
if [ $? -ne 0 ]; then
    echo "Failed to install Python dependencies. Check your Python and pip installation."
    exit 1
fi

# Check for Ollama CLI
if ! command -v ollama &> /dev/null
then
    echo "Ollama CLI is not installed. Please download it from https://ollama.ai/docs and add it to PATH."
    exit 1
fi

# Confirm setup
echo "Installation complete. Ready to run the Python script."
exit 0
