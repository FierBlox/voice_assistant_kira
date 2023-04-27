import sounddevice as sd 
import vosk  
import queue
import json
import commands
from functions import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

q = queue.Queue()

model = vosk.Model('model_small')

device = sd.default.device   #устройства ввода и вывода по умолчанию
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])  #частота дискретизации


#запись в очередь речи, если callback переполнился
def callback(indata, frames, time, status):
    q.put(bytes(indata))


def main():

    #векторное представление ключей
    vectoraizer = CountVectorizer()
    vectors = vectoraizer.fit_transform(list(commands.data_set.keys()))

    #соотношение ключей и значений
    clf = LogisticRegression()
    clf.fit(vectors, list(commands.data_set.values()))

    del commands.data_set

    #класс записывающий речь и обрабатывающий её, если человек перестал говорить
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16', channels=1, callback=callback):
        global data
        rec = vosk.KaldiRecognizer(model, samplerate)

        #бесконечный цикл записи речи
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
             data = json.loads(rec.Result())['text']
             recognize(data, vectoraizer, clf)


#функция вызывающая соответсвующую функцию
def recognize(data, vectoraizer, clf):

    #проверка на имя голосового помощника
    name = commands.NAME.intersection(data.split())
    if not name:
        return
    
    #замена имени на пустую строку
    data.replace(list(name)[0], "")

    #представление речи в векторах и их сравнение
    text_vector = vectoraizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    
    #вызов функции
    func_name = answer.split()[0]
    speaker(answer.replace(func_name, ""))
    exec(func_name + "()")
                
if __name__ == '__main__':
    main()