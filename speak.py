import os
import time
from gtts import gTTS #importing gTTS module for text to speech conversion
import playsound #importing playsound to play mp3 file

def speak(text):
    """
    This function takes in a string 'text' as an argument, converts it to speech using gTTS, 
    saves the speech as an mp3 file, and plays the mp3 file using playsound.
    """
    tts = gTTS(text=text, lang='en')
    filename = '.voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)

stop = False
while stop ==  False:
    """
    This while loop takes user input and continues to take input until the variable 'stop' is set to True.
    """
    text = input('Paste the text:   ')
    speak(text)


