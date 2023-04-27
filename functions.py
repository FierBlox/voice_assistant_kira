from api import api
from jokes import jokes
from random import randint
import webbrowser, pyttsx3, requests, sys

#настройки голоса помощника
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 180)
engine.setProperty('voice', voices[0].id)

#функция озвучивания речи
def speaker(text):
    engine.say(text)
    engine.runAndWait()

#функция, узнающая погоду
def weather():
 params = {'q': 'Tver', 'units': 'metric', 'lang': 'ru', 'appid': api}
 response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)

 #предтавление данных в виде списка
 w = response.json()
 speaker(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов" )

#открытие браузра по умолчанию
def browser():
    webbrowser.open("google.com", new=2)

#пустая функция, озвучивает то, что прописанов значения к ключам
def neutral():
    pass

#функция рассказывающая шутку
def joke():
 
 #выбор случайного индекса в списке шуток
 index = randint(0, len(jokes) - 1)
 speaker(jokes[index])

#выключение бота
def offbot():
    sys.exit()