**Requirements Document**

---

### Purpose
This document outlines the requirements for Windows and Linux users to run the provided Python code. The program facilitates a conversational interface between two models using prompts, with customization options for model selection, prompts, and conversation parameters.

---

### System Requirements

#### General Requirements
- Python 3.8 or higher
- Text editor or Integrated Development Environment (IDE)
- Internet connection (for dependencies installation)

#### Operating System Specific Requirements

##### Windows
- Windows 10 or higher
- Ensure Python is added to PATH during installation
- Terminal or Command Prompt with administrative privileges

##### Linux
- Any modern Linux distribution (e.g., Ubuntu 20.04+, Fedora, Debian)
- Terminal with appropriate permissions

---

### Software Requirements

#### Python Dependencies
Install the following Python libraries:
```bash
pip install subprocess-tee argparse textwrap logging
```
If `pip` is not installed, refer to your OS’s documentation to set it up.

#### External Requirements
- Ollama CLI installed and configured: [Ollama Documentation](https://ollama.ai/docs)
- JSON configuration file (`config.json`) with the following structure:

```json
{
    "model": ["model1", "model2", "model3"],
    "rand_prompt": ["prompt1", "prompt2"],
    "debate_topic": "topic"
}
```

---

### Installation Steps

#### Windows
1. Install Python from [python.org](https://www.python.org/downloads/).
2. Verify installation by running:
    ```bash
    python --version
    pip --version
    ```
3. Install required Python libraries:
    ```bash
    pip install subprocess-tee argparse textwrap logging
    ```
4. Download and install Ollama CLI for Windows.

#### Linux
1. Install Python:
    - Ubuntu/Debian:
      ```bash
      sudo apt update && sudo apt install python3 python3-pip -y
      ```
    - Fedora:
      ```bash
      sudo dnf install python3 python3-pip -y
      ```
2. Verify installation:
    ```bash
    python3 --version
    pip3 --version
    ```
3. Install required Python libraries:
    ```bash
    pip3 install subprocess-tee argparse textwrap logging
    ```
4. Download and install Ollama CLI for Linux.

---

### Usage Instructions

1. Ensure the `config.json` file exists in the same directory as the Python script.
2. Launch the script:
    - Windows:
      ```bash
      python script_name.py
      ```
    - Linux:
      ```bash
      python3 script_name.py
      ```
3. Follow the interactive prompts to:
    - Select models
    - Define prompts
    - Set conversation parameters
4. Begin the AI conversation or debate mode as per the menu.

---

### Known Issues and Troubleshooting

- **Missing `config.json`:** Ensure the configuration file exists and follows the correct JSON structure.
- **Ollama errors:** Verify Ollama CLI is correctly installed and accessible in the terminal.
- **Python version mismatch:** Confirm the Python version is 3.8 or higher.
- **Permission Denied:** Run the terminal as an administrator or root user.

---

### Future Enhancements
- Add support for advanced debate mode.
- Integrate automated error handling for missing dependencies.

