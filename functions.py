from api import api
import webbrowser, pyttsx3, requests, sys, pyjokes

from textblob import TextBlob

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
 joke = pyjokes.get_joke()
 print(joke)
 blob = TextBlob(joke)
 end = blob.translate(from_lang='en', to='ru')
 speaker(end)

def offbot():
    sys.exit()

def search():
   # webbrowser.open(f"https://yandex.ru/search/?text={request}", new=2)
    pass