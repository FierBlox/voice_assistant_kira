from api import api
from jokes import jokes
from random import randint
import webbrowser, pyttsx3, requests, sys

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 180)
engine.setProperty('voice', voices[0].id)

def speaker(text):
    engine.say(text)
    engine.runAndWait()

def weather():
 params = {'q': 'Tver', 'units': 'metric', 'lang': 'ru', 'appid': api}
 response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
 w = response.json()
 speaker(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов" )

def browser():
    webbrowser.open("google.com", new=2)

def neutral():
    pass

def joke():
 index = randint(0, len(jokes) - 1)
 speaker(jokes[index])

def offbot():
    sys.exit()