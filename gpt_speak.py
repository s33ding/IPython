
"""## Introduction
This code is a Python script for a conversational AI application. It uses the OpenAI API and other libraries such as termcolor, os, json, gTTS, and playsound to accomplish the following tasks:

1. Convert text to speech using gTTS and play it with playsound.
2. Load the API key from a JSON file and set it in the OpenAI API.
3. Ask a question to OpenAI's GPT-3 API, get the response, and print it.
4. Continuously take user input, convert it to speech, ask GPT-3 the input, get the response, and play it.
The conversational AI continues until the stop variable is set to True."""


# import the termcolor library
from termcolor import colored

import os
import json
import openai
import os
import time
from gtts import gTTS #importing gTTS module for text to speech conversion
import playsound #importing playsound to play mp3 file

prompt_gpt = f"\nGPT👽: "
prompt_me = f"\nME👻 >>> "

def speak(text):
    """
    This function takes in a string 'text' as an argument, converts it to speech using gTTS, 
    saves the speech as an mp3 file, and plays the mp3 file using playsound.
    """
    tts = gTTS(text=text, lang='en')
    filename = '.voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)



# Load the API key from the JSON file
with open(os.environ["OPENAI_API_KEY"],"r") as f:
    api_key = json.load(f)["api_key"]

openai.api_key = api_key

def ask_question_to_gpt3(message):
    # Load the API key from the JSON file
    with open(os.environ["OPENAI_API_KEY"],"r") as f:
        api_key = json.load(f)["api_key"]

    # Set the API key
    openai.api_key = api_key

    # Ask the question to GPT-3 and get the response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=message,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Get the response text
    txt = response["choices"][0]["text"]

    return txt

stop = False

while stop ==  False:
    """
    This while loop takes user input and continues to take input until the variable 'stop' is set to True.
    """
    text = input(colored(prompt_me,'red'))
    response = ask_question_to_gpt3(text)
    print(colored(f"{prompt_gpt}{response}", 'yellow'))
    speak(response)

