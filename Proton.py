import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import Gesture_Controller
#import Gesture_Controller_Gloved as Gesture_Controller
import app
from threading import Thread


# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# ----------------Variables------------------------
file_exp_status = False
files = []
path = ''
is_awake = True  # Bot status


# ------------------Functions----------------------
def reply(audio):
    app.ChatBot.addAppMsg(audio)
    print(audio)
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        reply("Good Morning!")
    elif hour >= 12 and hour < 18:
        reply("Good Afternoon!")
    else:
        reply("Good Evening!")

    reply("I am Proton, how may I help you?")


# 🎤 FIXED Audio to String
def record_audio():
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.adjust_for_ambient_noise(source, duration=1)  # important
        r.pause_threshold = 0.8

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=6)
        except:
            print("❌ Mic timeout")
            return ""

    try:
        voice_data = r.recognize_google(audio)
        print("✅ You said:", voice_data)
        return voice_data.lower()

    except sr.UnknownValueError:
        print("❌ Can't recognize speech")
        return ""

    except sr.RequestError as e:
        print("❌ Google API error:", e)
        return ""


# Executes Commands (input: string)
def respond(voice_data):
    global file_exp_status, files, is_awake, path

    print("COMMAND:", voice_data)
    voice_data = voice_data.replace('proton', '')  # FIXED
    app.eel.addUserMsg(voice_data)

    if is_awake == False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    elif 'hello' in voice_data:
        wish()

    elif 'what is your name' in voice_data:
        reply('My name is Proton!')

    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'search' in voice_data:
        reply('Searching for ' + voice_data.split('search')[1])
        url = 'https://google.com/search?q=' + voice_data.split('search')[1]
        try:
            webbrowser.open(url)
            reply('This is what I found')
        except:
            reply('Please check your Internet')

    elif 'bye' in voice_data:
        reply("Good bye! Have a nice day.")
        is_awake = False

    elif 'exit' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        sys.exit()

    elif 'launch gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            reply('Gesture recognition is already active')
        else:
            gc = Gesture_Controller.GestureController()
            t = Thread(target=gc.start)
            t.start()
            reply('Gesture recognition launched successfully')

    elif 'stop gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
            reply('Gesture recognition stopped')
        else:
            reply('Gesture recognition is already inactive')

    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')

    elif 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')

    else:
        reply('I am not functioned to do this!')


# ------------------Driver Code--------------------

t1 = Thread(target=app.ChatBot.start)
t1.start()

while not app.ChatBot.started:
    time.sleep(0.5)

wish()

while True:
    if app.ChatBot.isUserInput():
        voice_data = app.ChatBot.popUserInput()
    else:
        voice_data = record_audio()

    if voice_data and 'proton' in voice_data:
        try:
            respond(voice_data)
        except SystemExit:
            reply("Exit Successful")
            break
        except Exception as e:
            print("❌ ERROR:", e)
            break