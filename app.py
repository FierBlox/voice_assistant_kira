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


device = sd.default.device    

samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate']) 


def callback(indata, frames, time, status):

    q.put(bytes(indata))


def main():

    vectoraizer = CountVectorizer()
    vectors = vectoraizer.fit_transform(list(commands.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(commands.data_set.values()))

    del commands.data_set


    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16', channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
             data = json.loads(rec.Result())['text']
             recognize(data, vectoraizer, clf)


def recognize(data, vectoraizer, clf):
    name = commands.NAME.intersection(data.split())
    if not name:
        return
    data.replace(list(name)[0], "")
    text_vector = vectoraizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    
    func_name = answer.split()[0]
    speaker(answer.replace(func_name, ""))
    exec(func_name + "()")
                
if __name__ == '__main__':
    main()
