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
from pynput import keyboard


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r") as f:
        return json.load(f)
    
def scrolling_text(text, delay=0.03):
    """Prints text with a scrolling effect."""
    for char in text:
        if stop_flag:
            return
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
        sentences = re.split(r'(?<=[.!?])\s+', text)
        paragraphs = []
        for i in range(0, len(sentences), sentences_per_paragraph):
            paragraph = ' '.join(sentences[i:i+sentences_per_paragraph])
            paragraphs.append(paragraph)
    return paragraphs

def on_press(key):
    global stop_flag, conversation_active
    if conversation_active and key == keyboard.Key.esc:
        print("\nEscape key pressed! Exiting loop.\n")
        stop_flag = True

def query_model(model_name, prompt):
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

listener = keyboard.Listener(on_press=on_press)
listener.start()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

config = load_config()
model = config["model"]
rand_prompt = config["rand_prompt"]
debate_topic = config["debate_topic"]
debate_mode = "Off"
debate_rand = False
stop_flag = False
conversation_active = False
debate_input = ""
convo_num = rng.randint(10,500)
model1_choice = rng.randint(0,3)
model2_choice = rng.randint(0,3)
sleep_time = 1
instruction_list = config["instruction_key"]
instruction = " ".join(instruction_list)
# starting_list= config["starting_prompt"]
starting_prompt = "pick any random conversational topic, and add a one paragraph explination"  
debate_instruction = ""


while True:
    stop_flag = False
    conversation_active = False
    selection = input("""\nSelect one of the following:
                
                START 

                OPTIONS
                  
                QUIT 
                    
                Enter Selection: """)
    print("\n")
    
    match selection.upper():
        case "OPTIONS":
            while True:
                option_selection = input("""\nSelect the following:
                                         
                MODEL        (Model selections)
                
                PROMPT       (Initial prompt to start conversation)
                CONVO        (# of conversations between movels)
                INSTRUCTION  (specific behavior instructions for model)
                
                DEBATE       (Activate Debate Mode (On/Off))
                TOPIC        (Enter debate topic)      
                
                BACK         (Return to main menu)
               
                Enter Selection: """)
                match option_selection.upper():
                    case "MODEL":
                        print("\nCurrent models are randomly selected.")
                        choose_model = input("\nWould you like to choose the models? (Yes/No): ")
                        if choose_model.upper() == "YES":
                            print("Available models:", model)
                            model1_choice = input("Enter index of model 1: ")
                            model2_choice = input("Enter index of model 2: ")
                            print(f"Selected models: {model[int(model1_choice)]} and {model[int(model2_choice)]}")
                            time.sleep(3)
                        elif choose_model.upper() == "NO":
                            print("\nModels will stay randomly selected.\n")
                            time.sleep(3)
                        else:
                            print("\nInvalid selection.\n")
                            time.sleep(3)
                    case "PROMPT":
                        print(f"\nCurrent prompt: {starting_prompt}\n")
                        choose_prompt = input("\nWould you like to change the prompt? (Yes/No): ")
                        if choose_prompt.upper() == "YES":
                            starting_prompt = input("\nEnter starting prompt: ")
                            print("\nPrompt updated.\n")
                            time.sleep(3)
                        elif choose_prompt.upper() == "NO":
                            print("\nPrompt will stay the same.\n")
                            time.sleep(3)
                        else:
                            print("\nInvalid selection\n")
                            time.sleep(3)
                    case "CONVO":
                        print("\nCurrent number of conversations is random!\n")
                        convo_choice = input("\nWould you like to change the number of conversations? (Yes/No): ")
                        if convo_choice.upper() == "YES":
                            convo_num = input("Enter number of conversations: ")
                            print(f"\nNumber of conversations changed to {convo_num}.\n")
                            time.sleep(3)
                        elif convo_choice.upper() == "NO":
                            print("\nNumber of conversations will stay random.\n")
                            time.sleep(3)
                        else:
                            print("\nInvalid selection.\n")
                            time.sleep(3)
                    case "INSTRUCTION":
                        print(f"\nCurrent instruction: {instruction}\n")
                        instruciton_choice = input("\nWould you like to change the instruction? (Yes/No): ")
                        if instruciton_choice.upper() == "YES":
                            instruction = input("Enter instruction for model to follow: ")
                        elif instruciton_choice.upper() == "NO":
                            print("\nInstruction will stay the same.\n")
                            time.sleep(3)
                        else:
                            print("\nInvalid selection.\n")
                            time.sleep(3)
                    case "DEBATE":
                        print(f"\nDebate mode is currently {debate_mode}.\n")
                        debate_switch = input("\nDebate mode (On/Off): ")
                        if debate_switch.upper() == "ON":
                            debate_mode = "On"
                            debate_rand = True
                            print("Debate mode enabled.")
                            time.sleep(3)
                        elif debate_switch.upper() == "OFF":
                            debate_mode = "Off"
                            print("Debate mode disabled.")
                            time.sleep(3)
                        else:
                            print("\nInvalid selection. Please enter 'On' or 'Off'.\n")
                            time.sleep(3)
                    case "TOPIC":
                        if debate_mode == "Off":
                            print("Debate mode not enabled. \nplease enable debate mode to use this feature.\n")
                            time.sleep(3)
                        elif debate_mode == "On":
                            debate_choice = input("\nWould you like to enter a debate topic? (Yes/No): ")
                            if debate_choice.upper() == "YES":
                                debate_input = input("Enter debate topic: ")
                                print(f'Debate topic set to "{debate_input}".')
                                debate_rand = False
                                time.sleep(3)
                            elif debate_choice.upper() == "NO":
                                print("\nDebate topic will be picked randomly.\n")
                                debate_rand = True
                                time.sleep(3)
                            else:
                                print("\nInvalid selection.\n")
                                time.sleep(3)
                        else:
                            print("\nInvalid selection.\n")
                            time.sleep(3)
                    case "BACK":
                        break
        case "QUIT":
            print("Goodbye!")
            time.sleep(3)
            exit()
        case "START":
            

            def main():
                global instruction, stop_flag, conversation_active, starting_prompt, debate_instruction
                conversation_active = True
                # Parse arguments for conversation settings.
                parser = argparse.ArgumentParser(
                    description="Run a conversation between two Ollama models."
                )
                parser.add_argument(
                    "--model1",
                    default=model[int(model1_choice)],
                    help="First model to use in the conversation"
                )
                parser.add_argument(
                    "--model2",
                    default=model[int(model2_choice)],
                    help="Second model to use in the conversation"
                )
                parser.add_argument(
                    "--exchanges",
                    type=int,
                    default=int(convo_num),
                    help="Number of exchanges between the models"
                )
                parser.add_argument(
                    "--prompt",
                    default=starting_prompt,
                    help="Initial prompt to start the conversation"
                )
                
                args = parser.parse_args()
                
                if debate_mode == "On" and debate_rand == False:
                    starting_prompt = f"Debate the topic of {debate_input}."
                    instruction = instruction + f"ALWAYS debate the point opposite of the prompt, giving facts and the best evidence for your position, Never agree with the side of the prompt even if you believe it is true, work on debunking the prompt."
                    debate_instruction = instruction
                    current_prompt = starting_prompt
                elif debate_mode == "On" and debate_rand == True:
                    starting_prompt = f"debate the topic of {rng.choice(debate_topic)}"
                    instruction = instruction + f"debate the point opposite of the prompt, giving facts and the best evidence for your position "
                    debate_instruction = instruction
                    current_prompt = starting_prompt
                else:
                    current_prompt = args.prompt
                # current_prompt = args.prompt
                for i in range(args.exchanges):
                    if i >= args.exchanges - rng.randint(1,args.exchanges) and debate_mode == "Off":
                        instruction = instruction + f"""respond to the prompt as you normally would but incorporate the topic of 
                        {rng.choice(rand_prompt)} into the conversation seemlessly and relate the two.
                        make sure to tie them together in the conversation as smooth as possiable."""   
                    else:
                        instruction = instruction
                    
                    logging.info(f"Exchange {i + 1}/{args.exchanges}\n")
                    
                    # Query first model
                    response1 = query_model(args.model1, current_prompt)
                    if response1 is None or stop_flag:
                        logging.error("Conversation terminated.")
                        break
                    paragraphs1 = split_into_paragraphs(f"{args.model1}: {response1}", sentences_per_paragraph=4)
                   
                   
                    for para in paragraphs1:
                        if stop_flag:
                            break
                        wrapped_para = textwrap.fill(para, width=100)
                        scrolling_text(wrapped_para)
                        print()  # Add an extra line break between paragraphs
                    print("________________(press esc to end)________________ ")
                    print("\n")
                    
                    if stop_flag:
                        break                  
                    
                    
                    time.sleep(int(sleep_time))
                    


                    # Query second model with first model's response as prompt
                    response2 = query_model(args.model2, response1)
                    if response2 is None or stop_flag:
                        logging.error("Conversation terminated.")
                        break
                    paragraphs2 = split_into_paragraphs(f"{args.model2}: {response2}", sentences_per_paragraph=4)
                    
                    
                    for para in paragraphs2:
                        if stop_flag:
                            break
                        wrapped_para = textwrap.fill(para, width=100)
                        scrolling_text(wrapped_para)
                        print()  # Add an extra line break between paragraphs
                    print("________________(press esc to end)________________ ")
                    print("\n")
                    
                    if stop_flag:
                        break


                    time.sleep(int(sleep_time))
                    

                    
                    current_prompt = response2 + debate_instruction
                  
                conversation_active = False
                stop_flag = False
            if __name__ == "__main__":
                try:
                    main()
                except KeyboardInterrupt:
                    print("\nConversation terminated.")
                    stop_flag = True
                    conversation_active = False
                    continue
            

