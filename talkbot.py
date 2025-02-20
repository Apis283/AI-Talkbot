import subprocess
import argparse
import logging
import time
import sys
import textwrap
import re
import random as rng
import json 

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
        sentences = re.split(r'(?<=[.!?])\s+', text)
        paragraphs = []
        for i in range(0, len(sentences), sentences_per_paragraph):
            paragraph = ' '.join(sentences[i:i+sentences_per_paragraph])
            paragraphs.append(paragraph)
    return paragraphs

# List of available models
model = 
rand_prompt = 

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)



# Interactive inputs for conversation parameters
convo_num = rng.randint(10,500)
starting_prompt = "pick any random conversational topic, and add a one paragraph explination"
model1_choice = rng.randint(0,3)
model2_choice = rng.randint(0,3)
sleep_time = 1
instruction = """ when talking add some attitude and life to the conversation, 
be as informal as possiable, you can add in some phylosophical speech now and then but 
sound natural, dont say hey there or hey man all the time.repond to the prompt as you normally would incorporate a question about the 
conversation as seemlessly as possiable. """

while True:
    selection = input("""\nSelect the following:
                MODEL = Model selections
                PROMPT = Initial prompt to start conversation
                CONVO = # of conversations between movels
                SLEEP = Time waited between model responses
                INSTRUCTION = specific behavior instructions for model.
                DEBATE = Start AI Debate      
                DONE = Start AI Conversations
                      
                QUIT = Quit Program
                    
                Enter Selection: """)
    print("\n")
    match selection.upper():
        case "MODEL":
            print("Available models:", model)
            model1_choice = input("Enter index of model 1: ")
            model2_choice = input("Enter index of model 2: ")
        case "PROMPT":
            starting_prompt = input("Enter starting prompt: ")
        case "CONVO":
            convo_num = input("Enter number of conversations: ")
        case "SLEEP":
            sleep_time = input("Enter time waited between model responses (in seconds): ")
        case "INSTRUCTION":
            instruction = input("Enter instruction for model to follow: ")
        case "DEBATE":
            print("Debate mode not yet implemented.")
        case "QUIT":
            print("Goodbye!")
            exit()
        case "DONE":
            print(f"""
                  
                  The following settings will be applied: 
                 
                  -model 1 choice: {model[int(model1_choice)]}
                  -model 2 choice: {model[int(model2_choice)]}
                  -starting prompt: {starting_prompt}
                  -convo number: {convo_num}
                  -sleep time: {int(sleep_time)} seconds
                  -instruction: {instruction}
                  
                  """)
            




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

            def main():
                global instruction

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
                
                current_prompt = args.prompt
                for i in range(args.exchanges):
                    logging.info(f"Exchange {i + 1}/{args.exchanges}\n")
                    
                    # Query first model
                    response1 = query_model(args.model1, current_prompt)
                    if response1 is None:
                        logging.error("Conversation terminated due to error.")
                        break
                    paragraphs1 = split_into_paragraphs(f"{args.model1}: {response1}", sentences_per_paragraph=4)
                    for para in paragraphs1:
                        wrapped_para = textwrap.fill(para, width=100)
                        scrolling_text(wrapped_para)
                        print()  # Add an extra line break between paragraphs
                    print("________________(press spacebar to end)________________ ")
                    print("\n")
                    
                    time.sleep(int(sleep_time))
                    
                    # Query second model with first model's response as prompt
                    response2 = query_model(args.model2, response1)
                    if response2 is None:
                        logging.error("Conversation terminated due to error.")
                        break
                    paragraphs2 = split_into_paragraphs(f"{args.model2}: {response2}", sentences_per_paragraph=4)
                    for para in paragraphs2:
                        wrapped_para = textwrap.fill(para, width=100)
                        scrolling_text(wrapped_para)
                        print()  # Add an extra line break between paragraphs
                    print("________________(press spacebar to end)________________ ")
                    print("\n")
                    
                    time.sleep(int(sleep_time))
                    
                    if i >= args.exchanges - rng.randint(1,args.exchanges):
                        instruction = f"""when talking add some attitude and life to the conversation, be as informal as possiable, you can add in some phylosophical speech now and then but sound natural. repond to the prompt as you normally would but incorporate the topic of {rng.choice(rand_prompt)} into the conversation seemlessly and relate the two, make sure to tie them together in the conversation as smooth as possiable. repond to the prompt as you normally would incorporate a question about the conversation as seemlessly as possiable. """   
                    else:
                        instruction = instruction
                    #logging.info(f"Current instruction: {instruction}")
                    current_prompt = response2 
                  

            if __name__ == "__main__":
                main()
