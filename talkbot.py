import subprocess
import argparse
import logging
import time
import sys
import textwrap
import re
import random as rng
import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QComboBox,
    QSpinBox,
    QMessageBox,
)


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r") as f:
        return json.load(f)


def scrolling_text(text, delay=0.03):
    """Prints text with a scrolling effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # New line after text


def split_into_paragraphs(text, sentences_per_paragraph=4):
    """
    Splits text into paragraphs.
    If the text already contains double newlines, uses them as paragraph boundaries.
    Otherwise, splits into sentences (using punctuation) and groups them.
    """
    if "\n\n" in text:
        paragraphs = text.split("\n\n")
    else:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        paragraphs = []
        for i in range(0, len(sentences), sentences_per_paragraph):
            paragraph = " ".join(sentences[i : i + sentences_per_paragraph])
            paragraphs.append(paragraph)
    return paragraphs


# List of available models
config = load_config()
model = config["model"]
rand_prompt = config["rand_prompt"]
debate_topic = config["debate_topic"]
debate_mode = 0

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def query_model(model_name, prompt, instruction):
    """Query an Ollama model with a given prompt."""
    try:
        result = subprocess.run(
            ["ollama", "run", model_name, "prompt", prompt + instruction],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise Exception(result.stderr.strip())
        return result.stdout.strip()
    except Exception as e:
        logging.error(f"Error querying {model_name}: {e}")
        return None


def start_conversation(
    model1_choice,
    model2_choice,
    convo_num,
    starting_prompt,
    instruction,
    output_widget1,
    output_widget2,
):
    current_prompt = starting_prompt
    for i in range(convo_num):
        logging.info(f"Exchange {i + 1}/{convo_num}\n")

        # Query first model
        response1 = query_model(model1_choice, current_prompt, instruction)
        if response1 is None:
            logging.error("Conversation terminated due to error.")
            break
        paragraphs1 = split_into_paragraphs(
            f"{model1_choice}: {response1}", sentences_per_paragraph=4
        )
        for para in paragraphs1:
            wrapped_para = textwrap.fill(para, width=100)
            output_widget1.append(wrapped_para)
            output_widget1.append("\n")
        output_widget1.append(
            "________________(press spacebar to end)________________ "
        )
        output_widget1.append("\n")

        # Query second model with first model's response as prompt
        response2 = query_model(model2_choice, response1, instruction)
        if response2 is None:
            logging.error("Conversation terminated due to error.")
            break
        paragraphs2 = split_into_paragraphs(
            f"{model2_choice}: {response2}", sentences_per_paragraph=4
        )
        for para in paragraphs2:
            wrapped_para = textwrap.fill(para, width=100)
            output_widget2.append(wrapped_para)
            output_widget2.append("\n")
        output_widget2.append(
            "________________(press spacebar to end)________________ "
        )
        output_widget2.append("\n")

        if i >= convo_num - rng.randint(1, convo_num) and debate_mode == 0:
            instruction = f"""when talking add some attitude and life to the conversation, be as informal as possiable, you can add in some phylosophical speech now and then but sound natural. repond to the prompt as you normally would but incorporate the topic of {rng.choice(rand_prompt)} into the conversation seemlessly and relate the two, make sure to tie them together in the conversation as smooth as possiable. repond to the prompt as you normally would incorporate a question about the conversation as seemlessly as possiable. """
        elif debate_mode == 1:  # needs adjusting for debate mode
            instruction = debate_topic
        else:
            instruction = instruction
        current_prompt = response2


def create_main_window():
    app = QApplication(sys.argv)

    # Create a basic window
    window = QWidget()
    window.setWindowTitle("Talkbot Configuration")
    window.setGeometry(100, 100, 800, 600)  # x, y, width, height

    # Set the background color of the main window
    window.setStyleSheet("background-color: rgba(92, 105, 35, 255);")

    layout = QGridLayout()

    # Add a label to the window
    label = QLabel("Talkbot Configuration", window)
    layout.addWidget(label, 0, 0, 1, 2)

    # Add other widgets as needed
    model_label1 = QLabel("Model 1:", window)
    layout.addWidget(model_label1, 1, 0)

    model_combo1 = QComboBox(window)
    model_combo1.addItems(config["model"])
    layout.addWidget(model_combo1, 1, 1)

    model_label2 = QLabel("Model 2:", window)
    layout.addWidget(model_label2, 2, 0)

    model_combo2 = QComboBox(window)
    model_combo2.addItems(config["model"])
    layout.addWidget(model_combo2, 2, 1)

    prompt_label = QLabel("Starting Prompt:", window)
    layout.addWidget(prompt_label, 3, 0)

    prompt_input = QLineEdit(window)
    layout.addWidget(prompt_input, 3, 1)

    convo_label = QLabel("Number of Conversations:", window)
    layout.addWidget(convo_label, 4, 0)

    convo_spin = QSpinBox(window)
    convo_spin.setRange(1, 1000)
    layout.addWidget(convo_spin, 4, 1)

    instruction_label = QLabel("Instruction:", window)
    layout.addWidget(instruction_label, 5, 0)

    instruction_input = QTextEdit(window)
    layout.addWidget(instruction_input, 5, 1)

    # Create a QHBoxLayout for the buttons
    button_layout = QHBoxLayout()

    start_button = QPushButton("Start", window)
    start_button.setFixedWidth(100)  # Set fixed width for the start button
    start_button.setStyleSheet(
        "background-color: lightblue;"
    )  # Set background color for the start button
    button_layout.addWidget(start_button)

    layout.addLayout(button_layout, 6, 0, 1, 2)

    # Create a QHBoxLayout for the output widgets and their labels
    output_layout = QHBoxLayout()

    # Add a label and QTextEdit widget to display the conversation for model 1
    output_widget1_layout = QVBoxLayout()
    output_label1 = QLabel("Model 1 Output:", window)
    output_widget1 = QTextEdit(window)
    output_widget1.setReadOnly(True)
    output_widget1.setStyleSheet(
        "background-color: white;"
    )  # Set background color for the QTextEdit widget
    output_widget1_layout.addWidget(output_label1)
    output_widget1_layout.addWidget(output_widget1)

    # Add a label and QTextEdit widget to display the conversation for model 2
    output_widget2_layout = QVBoxLayout()
    output_label2 = QLabel("Model 2 Output:", window)
    output_widget2 = QTextEdit(window)
    output_widget2.setReadOnly(True)
    output_widget2.setStyleSheet(
        "background-color: white;"
    )  # Set background color for the QTextEdit widget
    output_widget2_layout.addWidget(output_label2)
    output_widget2_layout.addWidget(output_widget2)

    # Add the output widget layouts to the output_layout
    output_layout.addLayout(output_widget1_layout)
    output_layout.addLayout(output_widget2_layout)

    # Add the output_layout to the main layout
    layout.addLayout(output_layout, 7, 0, 1, 2)

    quit_button = QPushButton("Quit", window)
    quit_button.setFixedWidth(100)  # Set fixed width for the quit button
    quit_button.setStyleSheet(
        "background-color: lightcoral;"
    )  # Set background color for the quit button
    layout.addWidget(quit_button, 8, 0, 1, 2, alignment=Qt.AlignCenter)

    def on_quit_button_clicked():
        app.quit()

    quit_button.clicked.connect(on_quit_button_clicked)

    def on_start_button_clicked():
        model1_choice = model_combo1.currentText()
        model2_choice = model_combo2.currentText()
        starting_prompt = prompt_input.text()
        convo_num = convo_spin.value()
        instruction = instruction_input.toPlainText()

        start_conversation(
            model1_choice,
            model2_choice,
            convo_num,
            starting_prompt,
            instruction,
            output_widget1,
            output_widget2,
        )

    start_button.clicked.connect(on_start_button_clicked)

    window.setLayout(layout)

    # Show the window
    window.show()

    # Execute the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    create_main_window()
