import webbrowser, sys, requests, pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 180)
engine.setProperty('voice', voices[0].id)


def speaker(text):
    engine.say(text)
    engine.runAndWait()

def weather():
    pass

def browser():
    webbrowser.open("google.com", new=2)

def neutral():
    pass

def joke():
    print("Колобок повесился")

def offbot():
    sys.exit()

def search():
   # webbrowser.open(f"https://yandex.ru/search/?text={request}", new=2)
    pass