from allosaurus.app import read_recognizer
import tts.sapi
import os
import sys
import wave
import json

from vosk import Model, KaldiRecognizer, SetLogLevel
# !pip install vosk
import Word


def textToWav(text):
    voice = tts.sapi.Sapi()
    voice.create_recording('welcome.wav', text)

def findNext(target, words):
    i = 0
    data = []
    for word in words:
        if word[0]=='[' and i < len(words)-1:
            for element in target:
                if element['word'].lower() == words[i+1].lower():
                    timestamps = {}
                    timestamps['mood'] = word
                    timestamps['start'] = element['start']
                    data.append(timestamps)
        i += 1
    return data
                   


model_path = "./model"



data = input("Enter your Script here:- ")

list_of_words = data.split()


text = ' '.join(word for word in data.split() if word[0]!='[')
textToWav(text)

audio_filename = "./welcome.wav"

if not os.path.exists(model_path):
    print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as {model_path}")
    sys.exit()

model = Model(model_path)

if not os.path.exists(audio_filename):
    print(f"File '{audio_filename}' doesn't exist")
    sys.exit()

wf = wave.open(audio_filename, "rb")

rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

results = []

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        part_result = json.loads(rec.Result())
        results.append(part_result)

part_result = json.loads(rec.FinalResult())
results.append(part_result)



model = read_recognizer()


phoneme = model.recognize('./welcome.wav',timestamp=True)
grid_phoneme = [i.split() for i in phoneme.splitlines()]

moodTimeStamps = findNext(results[0]['result'],list_of_words)

print('phoneme:- ',phoneme)
print('moodTimestamp:- ',moodTimeStamps)

# Add the for loop here. Use the phoneme variable for Phoneme timestamp
# and moodTimeStamps variable for timestamp of moods.


print("completed")
